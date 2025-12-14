# Deployment Guide

## Quick Start

### Local Development

1. **Prerequisites:**
   ```bash
   # Python 3.9 or higher
   python --version
   
   # Redis (optional, for caching)
   redis-server --version
   ```

2. **Installation:**
   ```bash
   git clone https://github.com/mngenius/simple-data-explorer.git
   cd simple-data-explorer
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment template
   cp .env.example .env
   ```

3. **Create Sample Data:**
   ```bash
   python scripts/create_sample_data.py
   ```

4. **Run Application:**
   ```bash
   python run.py
   ```

5. **Access API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Query Endpoint: http://localhost:8000/api/v1/query/execute

### Docker Deployment

1. **Using Docker Compose (Recommended):**
   ```bash
   docker-compose up -d
   ```
   
   This starts:
   - API service on port 8000
   - Redis cache on port 6379

2. **Using Docker Only:**
   ```bash
   # Build image
   docker build -t simple-data-explorer:latest .
   
   # Run container
   docker run -d \
     -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     -e REDIS_HOST=localhost \
     -e ENABLE_CACHE=false \
     --name data-explorer \
     simple-data-explorer:latest
   ```

3. **View Logs:**
   ```bash
   docker-compose logs -f
   # or
   docker logs -f data-explorer
   ```

4. **Stop Services:**
   ```bash
   docker-compose down
   # or
   docker stop data-explorer && docker rm data-explorer
   ```

## Production Deployment

### Environment Configuration

Create a `.env` file with production values:

```bash
# Application
APP_NAME=Simple Data Explorer
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000

# Security (CHANGE THESE!)
SECRET_KEY=your-secure-random-secret-key-here-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
ENABLE_CACHE=true
CACHE_TTL=3600

# Query Engine
QUERY_ENGINE=duckdb
MAX_RESULT_ROWS=10000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
ENABLE_METRICS=true
```

### Kubernetes Deployment

1. **Create ConfigMap:**
   ```yaml
   # configmap.yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: data-explorer-config
   data:
     QUERY_ENGINE: "duckdb"
     ENABLE_CACHE: "true"
     LOG_LEVEL: "INFO"
   ```

2. **Create Secret:**
   ```yaml
   # secret.yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: data-explorer-secrets
   type: Opaque
   data:
     SECRET_KEY: <base64-encoded-secret>
     REDIS_PASSWORD: <base64-encoded-password>
   ```

3. **Create Deployment:**
   ```yaml
   # deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: data-explorer
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: data-explorer
     template:
       metadata:
         labels:
           app: data-explorer
       spec:
         containers:
         - name: api
           image: simple-data-explorer:latest
           ports:
           - containerPort: 8000
           envFrom:
           - configMapRef:
               name: data-explorer-config
           - secretRef:
               name: data-explorer-secrets
           volumeMounts:
           - name: data
             mountPath: /app/data
         volumes:
         - name: data
           persistentVolumeClaim:
             claimName: data-pvc
   ```

4. **Create Service:**
   ```yaml
   # service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: data-explorer
   spec:
     type: LoadBalancer
     ports:
     - port: 80
       targetPort: 8000
     selector:
       app: data-explorer
   ```

5. **Deploy:**
   ```bash
   kubectl apply -f configmap.yaml
   kubectl apply -f secret.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

### CDH/HDFS Integration

1. **Update Configuration:**
   ```bash
   # .env
   HDFS_URL=hdfs://your-hdfs-cluster:9000
   HIVE_METASTORE_URI=thrift://your-metastore:9083
   DATA_DIR=/hdfs/data/parquet
   ```

2. **Mount Hadoop Configuration:**
   ```yaml
   # In deployment.yaml
   volumeMounts:
   - name: hadoop-config
     mountPath: /etc/hadoop/conf
     readOnly: true
   
   volumes:
   - name: hadoop-config
     configMap:
       name: hadoop-config
   ```

3. **Configure Kerberos (if required):**
   ```yaml
   # In deployment.yaml
   env:
   - name: KRB5_CONFIG
     value: /etc/krb5.conf
   
   volumeMounts:
   - name: krb5-config
     mountPath: /etc/krb5.conf
     subPath: krb5.conf
   ```

## Scaling

### Horizontal Scaling

1. **Docker Compose:**
   ```bash
   docker-compose up -d --scale api=3
   ```

2. **Kubernetes:**
   ```bash
   kubectl scale deployment data-explorer --replicas=5
   ```

### Load Balancing

1. **Nginx Configuration:**
   ```nginx
   upstream data_explorer {
       least_conn;
       server api1:8000;
       server api2:8000;
       server api3:8000;
   }
   
   server {
       listen 80;
       
       location / {
           proxy_pass http://data_explorer;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **Health Check Configuration:**
   ```nginx
   location /health {
       proxy_pass http://data_explorer/health;
       access_log off;
   }
   ```

## Monitoring

### Prometheus Metrics

1. **Scrape Configuration:**
   ```yaml
   # prometheus.yml
   scrape_configs:
     - job_name: 'data-explorer'
       static_configs:
         - targets: ['data-explorer:9090']
   ```

2. **Access Metrics:**
   ```bash
   curl http://localhost:9090/metrics
   ```

### Grafana Dashboard

1. **Add Prometheus Data Source**
2. **Import Dashboard** (dashboard JSON to be created)
3. **Monitor:**
   - Request rate
   - Error rate
   - Response time
   - Cache hit rate

## Backup and Recovery

### Data Backup

```bash
# Backup Parquet files
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Backup Redis data (if using persistence)
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb redis-backup-$(date +%Y%m%d).rdb
```

### Disaster Recovery

1. **Restore Data:**
   ```bash
   tar -xzf data-backup-YYYYMMDD.tar.gz
   ```

2. **Restore Redis:**
   ```bash
   cp redis-backup-YYYYMMDD.rdb /var/lib/redis/dump.rdb
   redis-cli SHUTDOWN
   redis-server
   ```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS with valid certificates
- [ ] Configure CORS appropriately
- [ ] Set up authentication/authorization
- [ ] Enable Redis password
- [ ] Configure firewall rules
- [ ] Set up network policies (Kubernetes)
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Implement rate limiting

## Troubleshooting

### Common Issues

1. **Redis Connection Failed:**
   ```
   Solution: Set ENABLE_CACHE=false or fix Redis configuration
   ```

2. **Dataset Not Found:**
   ```
   Solution: Check DATA_DIR path and file permissions
   ```

3. **Port Already in Use:**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill <PID>
   ```

4. **Docker Build Fails:**
   ```bash
   # Clear Docker cache
   docker builder prune -a
   # Rebuild
   docker-compose build --no-cache
   ```

### Logs

1. **Application Logs:**
   ```bash
   # Docker
   docker-compose logs -f api
   
   # Kubernetes
   kubectl logs -f deployment/data-explorer
   ```

2. **Increase Log Level:**
   ```bash
   # In .env
   LOG_LEVEL=DEBUG
   ```

## Performance Tuning

### Query Optimization

1. **Partition Parquet Files:**
   ```python
   # By date
   df.to_parquet('data/sales.parquet', partition_cols=['date'])
   
   # By region
   df.to_parquet('data/sales.parquet', partition_cols=['region', 'date'])
   ```

2. **Adjust Cache TTL:**
   ```bash
   # In .env
   CACHE_TTL=7200  # 2 hours
   ```

3. **Increase Result Limit:**
   ```bash
   # In .env
   MAX_RESULT_ROWS=50000
   ```

### Resource Limits

1. **Docker Compose:**
   ```yaml
   # docker-compose.yml
   services:
     api:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
           reservations:
             cpus: '1'
             memory: 2G
   ```

2. **Kubernetes:**
   ```yaml
   # deployment.yaml
   resources:
     limits:
       cpu: "2"
       memory: "4Gi"
     requests:
       cpu: "1"
       memory: "2Gi"
   ```

## Support

For issues and questions:
- GitHub Issues: https://github.com/mngenius/simple-data-explorer/issues
- Documentation: http://localhost:8000/docs

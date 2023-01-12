**Deployment**

```bash
docker run -d world-backupper -e \
    S3_ENDPOINT_URL \
    S3_ACCESS_KEY \
    S3_SECRET_KEY \
    S3_BUCKET_NAME \
    BACKUP_TARGET_DIR \
    BACKUP_INTERVAL 
```
or use prepared .env file
```bash
docker run -d world-backupper --env-file .env
```

**Environment Variables**

_All listed bellow parameters required for start._

* `S3_ENDPOINT_URL` - The URL of the S3 endpoint to use.
* `S3_ACCESS_KEY` - The access key to use for the S3 endpoint. 
* `S3_SECRET_KEY` - The secret key to use for the S3 endpoint.
* `S3_BUCKET_NAME` - The name of the bucket to store the backups in.
* `BACKUP_TARGET_DIR` - The directory to back up.
* `BACKUP_INTERVAL` - The interval between backups. _(In minutes)_

**TODO**
* [ ] Add support for multiple files to backup
* [ ] Write tests
* [ ] Configuration file for storing env's
* [ ] Running multiple backups (async?)
* [ ] Upload .env template to repo
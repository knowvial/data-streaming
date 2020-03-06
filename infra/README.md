```shell
gcloud compute instances create data-streaming \
    --image-family debian-9 \
    --image-project debian-cloud \
    --zone us-west1-b \
    --tags all-data-streamimg \
    --network-interface=no-address \
    --metadata startup-script="#! /bin/bash
sudo apt-get update
sudo apt-get install apache2 -y
sudo service apache2 restart
echo '<!doctype html><html><body><h1>www-4</h1></body></html>' | tee /var/www/html/index.html
EOF"

gcloud compute firewall-rules create allow-for-data-streaming \
    --source-ranges 0.0.0.0/0 \
    --target-tags all-data-streamimg \
    --allow tcp:80-9999

gcloud compute instances describe instance-1 --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

---

```
gcloud compute firewall-rules update MY-RULE --allow tcp:80,icmp


gcloud compute ssh --project pulse-261908 --zone us-west1-b data-streaming



gcloud compute instances delete data-streaming

gcloud compute instances add-tags instance-1 --zone us-west1-b --tags all-data-streamimg

gcloud compute instances remove-tags instance-1 --all
```
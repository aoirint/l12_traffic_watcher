# l12_traffic_watcher

```shell
poetry export --without-hashes -o requirements.txt
```

```shell
docker build -t l12_traffic_watcher .

mkdir work
chown -R 1000:1000 work
docker run --rm --env-file ./.env -w /work -v "./work:/work" l12_traffic_watcher

docker run --rm --env-file ./.env  l12_traffic_watcher
```

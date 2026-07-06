# After cloning the repo, you can run the following commands to deploy the infrastructure: #

kubectl apply -f namespace.yaml
kubectl create secret generic postgres-secret \
  --namespace intern \
  --from-literal=db-name=appdb \
  --from-literal=db-user=appuser \
  --from-literal=db-password="appapssword"

kubectl apply -f postgres-configmap.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml
kubectl apply -f ingress.yaml

kubectl get pods -n intern


# To Run The Monitoring #

kubectl create namespace monitoring

helm install kube-prom prometheus-community/kube-prometheus-stack \
  -n monitoring \
  -f monitoring-values.yaml

kubectl apply -f flask-alerts.yaml

kubectl get pods -n monitoring -w

# Access the UIs #

http://<instance_public_ip>:30300   # Grafana (default login: admin / prom-operator)
http://<instance_public_ip>:30090   # Prometheus
http://<instance_public_ip>:30903   # Alertmanager


# Get the Grafana password if the default doesn't work: #

kubectl get secret -n monitoring kube-prom-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d



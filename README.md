# OnFinanceChatbot

## Chatbot API Documentation

### Overview
This API provides a chatbot service that processes user questions, retrieves relevant information from a Google Cloud Storage bucket, queries an external data source in BigQuery, and generates responses using OpenAI's GPT-3.5 model.

### Base URL
[http://34.138.121.239/chatbot](http://34.138.121.239/chatbot)

### Endpoints

1. **POST /chatbot**
   - **Description:** Process user questions and generate responses.
   - **Request Body:**
     ```json
     {
         "question": "Is 3M a capital-intensive business based on FY2022 data?"
     }
     ```
   - **Response:**
     ```json
     {
         "answer": "Based on the FY2022 data provided, 3M is a capital-intensive business. This can be inferred from the significant investment in property, plant, and equipment (PP&E) as shown in the Consolidated Balance Sheet. In 2022, 3M had a total of $9,178 million in net PP&E, which indicates a substantial amount of capital tied up in physical assets. Additionally, the cash flows from investing activities show that 3M made sizable purchases of PP&E in 2022, further supporting the conclusion that it is a capital-intensive business."
     }
     ```

2. **GET /**
   - **Description:** Display the homepage.
   - **Response:** A string indicating the homepage.

### Authentication
No authentication is required to access the API.

### Technologies Used
- Flask
- Google Cloud Storage
- Google BigQuery
- OpenAI GPT-3.5 model

### Kubernetes Cluster Details

```plaintext
kubectl get nodes
NAME                               STATUS   ROLES    AGE    VERSION
gk3-chatbot-pool-2-4bad0d0e-t8vk   Ready    <none>   6h3m   v1.27.8-gke.1067004

kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
chatbot-7c49485854-xwb2s          1/1     Running   0          4h11m

kubectl get services
NAME         TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
chatbot      LoadBalancer   34.118.226.193   34.138.121.239   80:30992/TCP   19h
kubernetes   ClusterIP      34.118.224.1     <none>           443/TCP        20h

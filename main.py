from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn
from scripts.monitor import monitoring_middleware

app = FastAPI()

# Add the monitoring middleware
app.middleware("http")(monitoring_middleware)

# Path to your GGUF model file
model_path = r"models/SQL_GEN_unsloth.Q8_0.gguf"

# Initialize the Llama model
model = Llama(
    model_path=model_path,  # Path to the GGUF model
    n_ctx=2048,             # Context window size
    n_threads=9,            # Number of CPU threads to use
    n_gpu_layers=20         # Number of layers to offload to GPU (if GPU is available)
)

class QueryRequest(BaseModel):
    question: str
    db_schema: str  # Renamed from 'schema' to 'db_schema'

@app.post("/generate-sql")
def generate_sql(query: QueryRequest):
    prompt = f"""
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    You are an SQL expert. Generate an SQL query based on the given question and database schema.

    ### Input:
    Question: {query.question}
    Schema: {query.db_schema}

    ### Response:
    """
    response = model(prompt, max_tokens=100, stop=["\n"], echo=True)
    return {"sql_query": response["choices"][0]["text"]}

# Run the API
if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
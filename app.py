from fastapi import FastAPI, HTTPException
from llama_cpp import Llama

# Load the GGUF model
model_path = "SQL_GEN_unsloth.Q8_0.gguf"  # Update with your model path
llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)

# Create FastAPI app
app = FastAPI()

@app.post("/generate")
async def generate(prompt: str, max_tokens: int = 100):
    try:
        # Generate text using the model
        response = llm(prompt, max_tokens=max_tokens, stop=["\n"], echo=False)
        return {"response": response["choices"][0]["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
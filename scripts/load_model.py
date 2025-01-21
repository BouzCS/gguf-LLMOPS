from llama_cpp import Llama

# Path to your GGUF model file
model_path = r"models/SQL_GEN_unsloth.Q8_0.gguf"

# Initialize the Llama model
model = Llama(
    model_path=model_path,  # Path to the GGUF model
    n_ctx=2048,             # Context window size
    n_threads=9,            # Number of CPU threads to use
    n_gpu_layers=20         # Number of layers to offload to GPU (if GPU is available)
)

# Generate text
prompt = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\nYou are an SQL expert, Generate an SQL query based on the given question and database schema and schema types.\n\n### Input:\nQuestion: What are the distinct ages of the heads who are acting?\nSchema: Table department has columns: Department_ID (number), Name (text), Creation (text), Ranking (number), Budget_in_Billions (number), Num_Employees (number) Table head has columns: head_ID (number), name (text), born_state (text), age (number) Table management has columns: department_ID (number), head_ID (number), temporary_acting (text) Column head_ID references column head_ID Column department_ID references column Department_ID Column Department_ID is a primary key Column head_ID is a primary key Column department_ID is a primary key\n\n### Response:\n"
response = model(prompt, max_tokens=100, stop=["\n"], echo=True)

# Print the response
print(response["choices"][0]["text"])
import pytest
from llama_cpp import Llama

def test_model_generation():
    # Load the model
    model_path = r"models/SQL_GEN_unsloth.Q8_0.gguf"
    model = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=9,
        n_gpu_layers=20
    )

    # Test prompt
    prompt = """
    Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    You are an SQL expert. Generate an SQL query based on the given question and database schema.

    ### Input:
    Question: What are the distinct ages of the heads who are acting?
    Schema: 
    Table department has columns: Department_ID (number), Name (text), Creation (text), Ranking (number), Budget_in_Billions (number), Num_Employees (number)
    Table head has columns: head_ID (number), name (text), born_state (text), age (number)
    Table management has columns: department_ID (number), head_ID (number), temporary_acting (text)
    Column head_ID references column head_ID
    Column department_ID references column Department_ID
    Column Department_ID is a primary key
    Column head_ID is a primary key
    Column department_ID is a primary key

    ### Response:
    """

    # Generate response
    response = model(prompt, max_tokens=100, stop=["\n"], echo=True)
    generated_sql = response["choices"][0]["text"]

    # Assert that the response is not empty
    assert generated_sql.strip() != "", "Model failed to generate SQL query."
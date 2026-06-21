from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
model = ChatHuggingFace(
    llm=HuggingFacePipeline.from_model_id(
        model_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        pipeline_kwargs={"max_length": 512, "temperature": 0.7}
    )
)
result = model.invoke("What is the capital of France?")
print(result.content)
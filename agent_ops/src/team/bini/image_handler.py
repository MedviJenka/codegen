import base64
from langchain_core.messages import HumanMessage
from agent_ops.src.utils.azure_llm import AzureLLMConfig


class CompressAndUploadImage(AzureLLMConfig):

    def upload_image(self, image_path: str, prompt: str = "Describe this image with as much detail as you can") -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ])

        response = self.langchain_llm.invoke([message])
        return str(response)

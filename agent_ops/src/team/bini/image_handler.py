import base64
from typing import Optional
from langchain_core.messages import HumanMessage
from agent_ops.src.utils.azure_llm import AzureLLMConfig


class CompressAndUploadImage(AzureLLMConfig):

    @staticmethod
    def __compress_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image

    def upload_image(self,
                     image_path: str,
                     sample_images: Optional[list[str]] = None,
                     prompt: str = "Describe this image with as much detail as you can") -> str:

        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.__compress_image(image_path=image_path)}"}}
        ])

        if sample_images:
            for each_sample_image in sample_images:
                sample = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.__compress_image(each_sample_image)}"}}
                message.append(sample)

        response = self.langchain_llm.invoke([message])
        return str(response)

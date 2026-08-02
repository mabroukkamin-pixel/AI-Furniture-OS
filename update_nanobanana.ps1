$file = "runtime\clients\nano_banana_client.py"

$content = Get-Content $file -Raw


$content = $content.Replace(
"self.client = None",
"self.client = None`n        self.model = None"
)


$content = $content.Replace(
"self.enabled = True",
"self.model = model`n            self.enabled = True"
)


$content = $content.Replace(
"model=GEMINI_MODEL",
"model=self.model"
)


$content = $content.Replace(
'''return {
                            "status": "success",
                            "image_path":
                                output_image_path,
                        }''',
'''return {
                            "status": "success",
                            "provider": "nano_banana",
                            "model": self.model,
                            "image_path": output_image_path,
                            "prompt_length": len(prompt),
                        }'''
)


Set-Content $file $content -Encoding UTF8

Write-Host "NanoBananaClient updated successfully"
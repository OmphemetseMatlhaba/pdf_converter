from django.shortcuts import render
from .forms import PDFUploadForm
from pdf2image import convert_from_path
import requests
import os
import uuid
from zipfile import ZipFile
from django.http import HttpResponse

def convert_pdf_view(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            output_folder = "media/converted"
            os.makedirs(output_folder, exist_ok=True)
            zip_path = os.path.join(output_folder, f"{uuid.uuid4()}.zip")

            with ZipFile(zip_path, 'w') as zipf:
                for f in files:
                    pdf_name = os.path.splitext(f.name)[0]
                    temp_pdf_path = os.path.join(output_folder, f.name)
                    with open(temp_pdf_path, 'wb+') as temp_file:
                        for chunk in f.chunks():
                            temp_file.write(chunk)

                    images = convert_from_path(temp_pdf_path, dpi=200)
                    for i, img in enumerate(images):
                        image_name = f"{pdf_name}_page_{i + 1}.png"
                        image_path = os.path.join(output_folder, image_name)
                        img.save(image_path, 'PNG')
                        zipf.write(image_path, arcname=image_name)

            with open(zip_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="converted_images.zip"'
                return response
    else:
        form = PDFUploadForm()

    return render(request, 'upload.html', {'form': form})




def get_advice(request):
    api_url = 'https://api.api-ninjas.com/v1/advice'
    api_key = 'lntEwUB2sHMblfZ4j2fkZA==mqGBRVhe51VFesRJ'  # Replace with your actual API key

    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    
    if response.status_code == requests.codes.ok:
        advice = response.json().get('advice', 'No advice found.')
    else:
        advice = f"Error: {response.status_code} - {response.text}"
    
    return render(request, 'advice.html', {'advice': advice})





import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def profanity_filter(request):
    profanity_result = None

    if request.method == 'POST':
        user_text = request.POST.get('text', '')

        api_url = 'https://api.api-ninjas.com/v1/profanityfilter'
        api_key = 'lntEwUB2sHMblfZ4j2fkZA==mqGBRVhe51VFesRJ'

        try:
            response = requests.get(
                api_url,
                headers={'X-Api-Key': api_key},
                params={'text': user_text}
            )

            print("Status Code:", response.status_code)
            print("Response Text:", response.text)

            if response.status_code == 200:
                data = response.json()
                profanity_result = data.get('censored', 'No result found.', )
            else:
                profanity_result = f"API Error: {response.status_code}"

        except Exception as e:
            profanity_result = f"Request Failed: {str(e)}"

    return render(request, 'profanity.html', {'result': profanity_result, })

   

    
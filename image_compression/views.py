from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse


# Create your views here.
def compress(request):
    user = request.user
    if request.method == "POST":
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
          original_img = form.cleaned_data["original_img"]
          quality = form.cleaned_data["quality"]

          compressed_image = form.save(commit=False) # temp item (don't want to mess with compressed img)
          compressed_image.user = user

          # perform compression
          img = Image.open(original_img)

          output_format = img.format
          buffer = io.BytesIO()
          # print("buffer => ", buffer.getvalue()) # b'' as in binary image data
          print("cursor position at the beginnig => ", buffer.tell())


          img.save(buffer, format=output_format, quality=quality)
          print("cursor position after the image compression => ", buffer.tell())
          
          buffer.seek(0) #should always be at the beginning to make the read and write operations / back to top
          print("cursor position after setting back to 0 => ", buffer.tell())

          # save the compressed image inside the model
          compressed_image.compressed_img.save(
              f'comressed_{original_img}', buffer
          )

          # Automatically download the compressed file
          response = HttpResponse(buffer.getvalue(), content_type=f"image/{output_format.lower()}")
          response["Content-Disposition"] = f"attachment; filename=comressed_{original_img}"
          return response



          # return redirect("compress")

    else:
        form = CompressImageForm()
        context = {
          "form": form,
        }
        return render(request, "image_compression/compress.html", context)
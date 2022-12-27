FROM public.ecr.aws/lambda/python:3.9

RUN yum update -y
# RUN yum install \
#     ffmpeg libsm6 libxext6 -y
RUN yum install -y mesa-libGL

# WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

# TODO: can potentially run uvicorn command override with handler command in template.yml
CMD ["main.handler"]
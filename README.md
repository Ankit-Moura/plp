step 1 > setup aws sso login 

now you should have awscli v2 in ur machine if you followed the first step correctly 

now log onto aws profile development-2xxxxxx using awscli

run pip install -r requirements.txt

finally run python s3_download.py to download all the files in plp bucket (should take around 5 mins)

lastly run python decomp.py to unzip everything into json format (takes a lot of time ~10 to 14)

if anything goes i will be sleeping :/ 
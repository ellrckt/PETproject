# from fastapi import APIRouter, UploadFile, File, HTTPException
# import os
# from schemas.profiles.profile import EditProfile, Profile

# profiles = APIRouter(tags=["profiles"], prefix="/profile")

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @profiles.post("/edit_profile", response_model=Profile)
# async def edit_profile(schema: EditProfile):
#     profile_dict = schema.dict(exclude_unset=True)
#     return Profile(
#         profile_img=profile_dict["profile_img"],
#         username=profile_dict["username"],
#         email=profile_dict["email"],
#     )


# @profiles.post("/uploadfile")
# async def uploadfile(file_uploaded: UploadFile = File(...)):
#     try:
#         file_name = file_uploaded.filename
#         file_path = os.path.join(UPLOAD_DIR, file_name)

#         with open(file_path, "wb") as f:
#             content = await file_uploaded.read()
#             f.write(content)

#         return {"filename": file_name, "message": "File uploaded successfully"}
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred while uploading the file: {e}"
#         )

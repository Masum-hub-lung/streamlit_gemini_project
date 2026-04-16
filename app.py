import streamlit as st
from api_calling import note_generator,audio_transcription,quiz_generator
from PIL import Image

st.title("Note summary and Quiz Generator")
st.markdown("upload upto 3 images to generate Note summary and Quizzes")
st.divider()


with st.sidebar:
    st.header("Controls")
    images = st.file_uploader(
        "Upload the photos of your note",
        type=['jpg','jpeg','png'],
        accept_multiple_files=True
    )
        
    pil_images = []
    
    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)
        
        
    if images:
        if len(images)>3:
            st.error("upload at max 3 images")
        else:
            col = st.columns(len(images))
            
            st.subheader("Uploaded images")
            
            for i,img in enumerate(images):
                with col[i]:
                     st.image(img)
        
    #difficulty
    selected_option = st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy","Medium","Hard"),
        index = None
    )  
    
    if selected_option:
        st.markdown(f"You selected **{selected_option}** as difficulty of your quiz")
    else:
        st.error("you must select a difficulty")
        
    pressed = st.button("Click the button to initiate AI",type="primary")

if pressed:
    if not images:
        st.error("you must upload one image")
    if not selected_option:
        st.error("you must select a difficulty")    
        
    if images and selected_option:
        
        #note
        
        with st.container(border=True):
            st.subheader("Your note")
            
            with st.spinner("AI is writiing notes for you"):
                #the portion below will be replaced by API call
                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)
            
        #Audio transipt
        
        with st.container(border=True):
            st.subheader("Audio Transcription")
            
            with st.spinner("AI is creating audio for you"):
                
                #clearing the markdown
                
                generated_notes = generated_notes.replace("#","")
                generated_notes = generated_notes.replace("*","")
                generated_notes = generated_notes.replace("-","")
                generated_notes = generated_notes.replace("`","")
                
                #the portion below will be replaced by API call
                audio_transcript = audio_transcription(generated_notes)
                st.audio(audio_transcript)
            
        #quiz    
        
        with st.container(border=True):
            st.subheader(f"Quiz ({selected_option}) Difficulty")
            
            #the portion below will be replaced by API call
            with st.spinner("AI is generating quizzes for you"):
                quizzes = quiz_generator(pil_images,selected_option)
                st.markdown(quizzes)    
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import *


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


def faiss_vector_db(data):
    # docs = dir_loader.load()
    docs = data
    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    # inp_txt = txt_splitter.split_documents(docs)
    inp_txt = txt_splitter.create_documents([docs])
    hfembeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDER,
        model_kwargs={'device': 'cpu'}
    )

    db = FAISS.from_documents(inp_txt, hfembeddings)
    db.save_local(VECTOR_DB_PATH)
    print(1)
    return "Vector Store Creation Completed"

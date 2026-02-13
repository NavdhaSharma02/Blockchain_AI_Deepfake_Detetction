import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from services.hash_service import HashService
from services.blockchain_service import BlockchainService
from services.ai_service import DeepfakeDetector
from database.database import init_db, get_db, VerificationRecord

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Blockchain AI Deepfake Detection API",
    description="Web3-enabled media authenticity verification system",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
hash_service = HashService()
blockchain_service = BlockchainService()
ai_detector = DeepfakeDetector(
    confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
)

# Create upload directory
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize database
init_db()

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 Starting Blockchain AI Deepfake Detection API...")
    print(f"📁 Upload directory: {UPLOAD_DIR}")
    print(f"🔗 Blockchain connected: {blockchain_service.is_connected()}")
    print(f"🤖 AI detector initialized on device: {ai_detector.device}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Blockchain AI Deepfake Detection API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "blockchain_connected": blockchain_service.is_connected(),
        "ai_model_loaded": ai_detector.model is not None
    }

@app.post("/api/verify")
async def verify_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verify media file authenticity
    
    Process:
    1. Generate SHA-256 hash of uploaded file
    2. Check blockchain for existing authenticity record
    3. If not found, run AI deepfake detection
    4. Return verification results
    """
    
    # Validate file type
    allowed_extensions = {
        '.jpg', '.jpeg', '.png', '.bmp', '.gif',  # Images
        '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv',  # Videos
        '.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac'  # Audio
    }
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Determine media type
    if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}:
        media_type = "image"
    elif file_ext in {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}:
        media_type = "video"
    else:
        media_type = "audio"
    
    try:
        # Save uploaded file temporarily
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Generate hash
        media_hash = hash_service.generate_file_hash(file_path)
        print(f"📝 Generated hash: {media_hash}")
        
        # Check if already verified in database
        existing_record = db.query(VerificationRecord).filter(
            VerificationRecord.media_hash == media_hash
        ).first()
        
        if existing_record:
            print(f"📚 Found existing record in database")
            return JSONResponse(content={
                "success": True,
                "cached": True,
                "media_hash": media_hash,
                "verification": existing_record.to_dict()
            })
        
        # Check blockchain
        print(f"🔗 Checking blockchain...")
        blockchain_result = blockchain_service.verify_media(media_hash)
        
        # Initialize result object
        result = {
            "media_hash": media_hash,
            "file_name": file.filename,
            "file_type": media_type,
            "blockchain_verified": blockchain_result.get("exists", False),
        }
        
        # If verified on blockchain
        if blockchain_result.get("exists"):
            print(f"✅ Media verified on blockchain")
            result.update({
                "status": "Verified Authentic",
                "blockchain_uploader": blockchain_result.get("uploader"),
                "blockchain_timestamp": blockchain_result.get("timestamp"),
                "message": "Media is registered on blockchain as authentic"
            })
            
            # Save to database
            record = VerificationRecord(
                media_hash=media_hash,
                file_name=file.filename,
                file_type=media_type,
                blockchain_verified=True,
                blockchain_uploader=blockchain_result.get("uploader"),
                blockchain_timestamp=blockchain_result.get("timestamp")
            )
            db.add(record)
            db.commit()
        
        else:
            # Run AI detection
            print(f"🤖 Running AI deepfake detection...")
            ai_result = ai_detector.detect(str(file_path), media_type)
            
            if "error" in ai_result:
                raise HTTPException(status_code=500, detail=ai_result["error"])
            
            result.update({
                "status": f"AI-Detected {ai_result['classification']}",
                "ai_classification": ai_result["classification"],
                "ai_confidence": ai_result["confidence_score"],
                "fake_probability": ai_result.get("fake_probability"),
                "real_probability": ai_result.get("real_probability"),
                "is_deepfake": ai_result.get("is_deepfake"),
                "ai_details": ai_result.get("details"),
                "message": f"AI classified as {ai_result['classification']} with {ai_result['confidence_score']}% confidence"
            })
            
            # Save to database
            record = VerificationRecord(
                media_hash=media_hash,
                file_name=file.filename,
                file_type=media_type,
                blockchain_verified=False,
                ai_classification=ai_result["classification"],
                ai_confidence=ai_result["confidence_score"],
                fake_probability=ai_result.get("fake_probability"),
                real_probability=ai_result.get("real_probability")
            )
            db.add(record)
            db.commit()
        
        # Clean up temporary file
        file_path.unlink()
        
        return JSONResponse(content={
            "success": True,
            "verification": result
        })
    
    except Exception as e:
        # Clean up on error
        if file_path.exists():
            file_path.unlink()
        
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify/image")
async def verify_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verify image file authenticity using Image Model
    Specialized endpoint for image deepfake detection
    """
    # Validate file type
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save and process
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        media_hash = hash_service.generate_file_hash(file_path)
        
        # Check cache
        existing_record = db.query(VerificationRecord).filter(
            VerificationRecord.media_hash == media_hash
        ).first()
        
        if existing_record:
            return JSONResponse(content={
                "success": True,
                "cached": True,
                "media_hash": media_hash,
                "verification": existing_record.to_dict()
            })
        
        # Run image detection
        print(f"🤖 Running Image Model detection...")
        ai_result = ai_detector.detect_image(str(file_path))
        
        if "error" in ai_result:
            raise HTTPException(status_code=500, detail=ai_result["error"])
        
        result = {
            "media_hash": media_hash,
            "file_name": file.filename,
            "file_type": "image",
            "blockchain_verified": False,
            "status": f"AI-Detected {ai_result['classification']}",
            "ai_classification": ai_result["classification"],
            "ai_confidence": ai_result["confidence_score"],
            "fake_probability": ai_result.get("fake_probability"),
            "real_probability": ai_result.get("real_probability"),
            "is_deepfake": ai_result.get("is_deepfake"),
            "ai_details": ai_result.get("details"),
            "message": f"Image analyzed with {ai_result['confidence_score']}% confidence"
        }
        
        # Save to database
        record = VerificationRecord(
            media_hash=media_hash,
            file_name=file.filename,
            file_type="image",
            blockchain_verified=False,
            ai_classification=ai_result["classification"],
            ai_confidence=ai_result["confidence_score"],
            fake_probability=ai_result.get("fake_probability"),
            real_probability=ai_result.get("real_probability")
        )
        db.add(record)
        db.commit()
        
        file_path.unlink()
        return JSONResponse(content={"success": True, "verification": result})
    
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify/video")
async def verify_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verify video file authenticity using Video Model
    Specialized endpoint for video deepfake detection
    """
    # Validate file type
    allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported video type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save and process
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        media_hash = hash_service.generate_file_hash(file_path)
        
        # Check cache
        existing_record = db.query(VerificationRecord).filter(
            VerificationRecord.media_hash == media_hash
        ).first()
        
        if existing_record:
            return JSONResponse(content={
                "success": True,
                "cached": True,
                "media_hash": media_hash,
                "verification": existing_record.to_dict()
            })
        
        # Run video detection
        print(f"🤖 Running Video Model detection...")
        ai_result = ai_detector.detect_video(str(file_path))
        
        if "error" in ai_result:
            raise HTTPException(status_code=500, detail=ai_result["error"])
        
        result = {
            "media_hash": media_hash,
            "file_name": file.filename,
            "file_type": "video",
            "blockchain_verified": False,
            "status": f"AI-Detected {ai_result['classification']}",
            "ai_classification": ai_result["classification"],
            "ai_confidence": ai_result["confidence_score"],
            "fake_probability": ai_result.get("fake_probability"),
            "real_probability": ai_result.get("real_probability"),
            "is_deepfake": ai_result.get("is_deepfake"),
            "ai_details": ai_result.get("details"),
            "message": f"Video analyzed with {ai_result['confidence_score']}% confidence"
        }
        
        # Save to database
        record = VerificationRecord(
            media_hash=media_hash,
            file_name=file.filename,
            file_type="video",
            blockchain_verified=False,
            ai_classification=ai_result["classification"],
            ai_confidence=ai_result["confidence_score"],
            fake_probability=ai_result.get("fake_probability"),
            real_probability=ai_result.get("real_probability")
        )
        db.add(record)
        db.commit()
        
        file_path.unlink()
        return JSONResponse(content={"success": True, "verification": result})
    
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify/audio")
async def verify_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verify audio file authenticity using Audio Model
    Specialized endpoint for audio deepfake detection
    """
    # Validate file type
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save and process
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        media_hash = hash_service.generate_file_hash(file_path)
        
        # Check cache
        existing_record = db.query(VerificationRecord).filter(
            VerificationRecord.media_hash == media_hash
        ).first()
        
        if existing_record:
            return JSONResponse(content={
                "success": True,
                "cached": True,
                "media_hash": media_hash,
                "verification": existing_record.to_dict()
            })
        
        # Run audio detection
        print(f"🤖 Running Audio Model detection...")
        ai_result = ai_detector.detect_audio(str(file_path))
        
        if "error" in ai_result:
            raise HTTPException(status_code=500, detail=ai_result["error"])
        
        result = {
            "media_hash": media_hash,
            "file_name": file.filename,
            "file_type": "audio",
            "blockchain_verified": False,
            "status": f"AI-Detected {ai_result['classification']}",
            "ai_classification": ai_result["classification"],
            "ai_confidence": ai_result["confidence_score"],
            "fake_probability": ai_result.get("fake_probability"),
            "real_probability": ai_result.get("real_probability"),
            "is_deepfake": ai_result.get("is_deepfake"),
            "ai_details": ai_result.get("details"),
            "message": f"Audio analyzed with {ai_result['confidence_score']}% confidence"
        }
        
        # Save to database
        record = VerificationRecord(
            media_hash=media_hash,
            file_name=file.filename,
            file_type="audio",
            blockchain_verified=False,
            ai_classification=ai_result["classification"],
            ai_confidence=ai_result["confidence_score"],
            fake_probability=ai_result.get("fake_probability"),
            real_probability=ai_result.get("real_probability")
        )
        db.add(record)
        db.commit()
        
        file_path.unlink()
        return JSONResponse(content={"success": True, "verification": result})
    
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/register")
async def register_media(
    media_hash: str,
    metadata: Optional[str] = "",
    db: Session = Depends(get_db)
):
    """
    Register media hash on blockchain
    
    Args:
        media_hash: SHA-256 hash of the media
        metadata: Optional metadata JSON string
    """
    
    try:
        print(f"📝 Registering hash on blockchain: {media_hash}")
        result = blockchain_service.register_media(media_hash, metadata)
        
        if result.get("success"):
            # Update database record
            record = db.query(VerificationRecord).filter(
                VerificationRecord.media_hash == media_hash
            ).first()
            
            if record:
                record.blockchain_verified = True
                db.commit()
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    
    total_verifications = db.query(VerificationRecord).count()
    blockchain_verified_count = db.query(VerificationRecord).filter(
        VerificationRecord.blockchain_verified == True
    ).count()
    ai_detected_count = db.query(VerificationRecord).filter(
        VerificationRecord.ai_classification != None
    ).count()
    
    blockchain_stats = blockchain_service.get_registry_stats()
    
    return {
        "total_verifications": total_verifications,
        "blockchain_verified": blockchain_verified_count,
        "ai_detected": ai_detected_count,
        "blockchain_registry": blockchain_stats
    }

@app.get("/api/history")
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent verification history"""
    
    records = db.query(VerificationRecord).order_by(
        VerificationRecord.created_at.desc()
    ).limit(limit).all()
    
    return {
        "history": [record.to_dict() for record in records]
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

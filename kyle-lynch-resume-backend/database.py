import aiosqlite
import json
from typing import Optional, List
from pathlib import Path
from datetime import datetime
import uuid

DB_PATH = Path(__file__).parent / "resume.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        """)
        await db.commit()

class ResumeDatabase:
    @staticmethod
    async def get_resume() -> Optional[dict]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT data FROM resumes WHERE id = 'main'")
            row = await cursor.fetchone()
            if row:
                return json.loads(row['data'])
            from data.mock import resumeData
            await ResumeDatabase.create_default_resume()
            return resumeData
    
    @staticmethod
    async def create_default_resume():
        from data.mock import resumeData
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO resumes (id, data, updated_at) VALUES (?, ?, ?)",
                ('main', json.dumps(resumeData), datetime.utcnow().isoformat())
            )
            await db.commit()
    
    @staticmethod
    async def update_personal_info(personal_info: dict) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume:
                return False
            if 'personal_info' not in resume:
                resume['personal_info'] = {}
            resume['personal_info'].update(personal_info)
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def update_highlights(highlights: list) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume:
                return False
            resume['highlights'] = highlights
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def update_skills(skills: list) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume:
                return False
            resume['skills'] = skills
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def get_experiences() -> List[dict]:
        resume = await ResumeDatabase.get_resume()
        return resume.get('experience', []) if resume else []
    
    @staticmethod
    async def add_experience(experience: dict) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume:
                return False
            if 'experience' not in resume:
                resume['experience'] = []
            resume['experience'].append(experience)
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def update_experience(exp_id: str, update_data: dict) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume or 'experience' not in resume:
                return False
            for exp in resume['experience']:
                if exp.get('id') == exp_id:
                    exp.update(update_data)
                    exp['updated_at'] = datetime.utcnow().isoformat()
                    async with aiosqlite.connect(DB_PATH) as db:
                        await db.execute(
                            "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                            (json.dumps(resume), datetime.utcnow().isoformat())
                        )
                        await db.commit()
                    return True
            return False
        except:
            return False
    
    @staticmethod
    async def delete_experience(exp_id: str) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume or 'experience' not in resume:
                return False
            original_count = len(resume['experience'])
            resume['experience'] = [exp for exp in resume['experience'] if exp.get('id') != exp_id]
            if len(resume['experience']) == original_count:
                return False
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def get_education() -> List[dict]:
        resume = await ResumeDatabase.get_resume()
        return resume.get('education', []) if resume else []
    
    @staticmethod
    async def add_education(education: dict) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume:
                return False
            if 'education' not in resume:
                resume['education'] = []
            resume['education'].append(education)
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False
    
    @staticmethod
    async def update_education(edu_id: str, update_data: dict) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume or 'education' not in resume:
                return False
            for edu in resume['education']:
                if edu.get('id') == edu_id:
                    edu.update(update_data)
                    edu['updated_at'] = datetime.utcnow().isoformat()
                    async with aiosqlite.connect(DB_PATH) as db:
                        await db.execute(
                            "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                            (json.dumps(resume), datetime.utcnow().isoformat())
                        )
                        await db.commit()
                    return True
            return False
        except:
            return False
    
    @staticmethod
    async def delete_education(edu_id: str) -> bool:
        try:
            resume = await ResumeDatabase.get_resume()
            if not resume or 'education' not in resume:
                return False
            original_count = len(resume['education'])
            resume['education'] = [edu for edu in resume['education'] if edu.get('id') != edu_id]
            if len(resume['education']) == original_count:
                return False
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    "UPDATE resumes SET data = ?, updated_at = ? WHERE id = 'main'",
                    (json.dumps(resume), datetime.utcnow().isoformat())
                )
                await db.commit()
            return True
        except:
            return False

class ContactDatabase:
    @staticmethod
    async def save_contact_message(message_data: dict) -> str:
        message_id = message_data.get('id', str(uuid.uuid4()))
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT INTO contact_messages 
                (id, name, email, subject, message, is_read, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                message_data['name'],
                message_data['email'],
                message_data['subject'],
                message_data['message'],
                0,
                message_data.get('created_at', datetime.utcnow().isoformat())
            ))
            await db.commit()
        return message_id
    
    @staticmethod
    async def get_contact_messages(limit: int = 50) -> List[dict]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM contact_messages 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            messages = []
            for row in rows:
                messages.append({
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'subject': row['subject'],
                    'message': row['message'],
                    'is_read': bool(row['is_read']),
                    'created_at': row['created_at']
                })
            return messages
    
    @staticmethod
    async def mark_message_as_read(message_id: str) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE contact_messages SET is_read = 1 WHERE id = ?",
                (message_id,)
            )
            await db.commit()
            return True

class UserDatabase:
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[dict]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    async def create_user(user_data: dict) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT INTO users (username, email, hashed_password, role, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_data['username'],
                user_data['email'],
                user_data['hashed_password'],
                user_data['role'],
                user_data.get('created_at', datetime.utcnow().isoformat()),
                user_data.get('last_login')
            ))
            await db.commit()
        return True
    
    @staticmethod
    async def update_last_login(username: str) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (datetime.utcnow().isoformat(), username)
            )
            await db.commit()
        return True
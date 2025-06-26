from redis_om import (Field, JsonModel)
import json
from typing import List
from redis_setup.entities import *

def build_db() -> bool:
    data : dict = json.load(open("./redis_setup/db.json"))
    
    try:
        User.delete_many(User.all_pks())
        Company.delete_many(Company.all_pks())
        Post.delete_many(Post.all_pks())
        Comment.delete_many(Company.all_pks())
        print("Database Cleared Successfully")
    except Exception as e:
        print(f"Error Cleaning Dataase: {e}")
        return False
    
    print(type(data))

    keys = data.keys()
    print(f"Keys to process: {keys}")
    
    try:
        for key in keys:
            if key.startswith("user:"):
                user = User.from_json(data[key])
                user.save()
            elif key.startswith("company:"):
                company = Company.from_json(data[key])
                company.save()
            elif key.startswith("post:"):
                post = Post.from_json(data[key])
                post.save()
            elif key.startswith("comment:"):
                comment = Comment.from_json(data[key])
                comment.save()

    except Exception as e:
        print(f"Error Building Dataase: {e}")
        return False
  
    print("Database Built Successfully")
    
    return True
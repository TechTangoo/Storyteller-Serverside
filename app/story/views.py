from flask import request, jsonify, send_file
from . import story_bp
from openai import OpenAI
from pathlib import Path

# * input: userid, description, title, category, imgurl
apikey = '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'


@story_bp.route("/create", methods=['POST'])
def create():
    try:
        from app import Supabase  # * Import Supabase here to avoid circular import
        data = request.get_json() or {}
        userid = data.get('userid')
        # * check for user
        user_data_res = Supabase.table('User').select(
            'user_id').eq('user_id', userid).eq('enabled', True).execute()
        if user_data_res.data is None:
            return jsonify({'status': 0, 'message': 'Author does not exist'}), 400
        # * get all the variables for request body for query
        # ! Also check for all the fields to exist
        title = data.get('title')
        if title is None:
            return jsonify({'status': 0, 'message': 'Missing object: title'}), 400
        description = data.get('description')
        if description is None:
            return jsonify({'status': 0, 'message': 'Missing object: description'}), 400
        category = data.get('category')
        if category is None:
            return jsonify({'status': 0, 'message': 'Missing object: category'}), 400
        imgurl = data.get('imgurl')
        if imgurl is None:
            return jsonify({'status': 0, 'message': 'Missing object: imgurl'}), 400
        # * request body for create query
        story_body = {
            'author': userid,
            'title': title,
            'description': description,
            'category': category,
            'imgurl': {'img': imgurl, 'index': 0}
        }
        # * create query
        create_query = Supabase.table('Story').insert(story_body).execute()

        # * check if query is successfully executed or not
        if create_query.data:
            return jsonify({'status': 1, 'message': 'Successfully created'}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to create story'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

# * to get story by storyid


@story_bp.route("/<string:storyid>", methods=['GET'])
def get_story(storyid):
    try:
        from app import Supabase  # * to avoid circular error
        # * fetch query
        story_query = Supabase.table('Story').select(
            "*",
            "User(*)"
        ).eq('story_id', storyid).eq('enabled', True).execute()

        if story_query.data:
            return jsonify({'status': 1, 'data': 0 / story_query.data}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to fetch story with given storyid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500


# * get all stories from userid

@story_bp.route("/user/<string:userid>", methods=['GET'])
def get_user_story(userid):
    try:
        from app import Supabase  # * to avoid circular error
        # * fetch query
        story_query = Supabase.table('Story').select(
            "*",
            "User(*)"
        ).eq('author', userid).eq('enabled', True).execute()

        if story_query.data:
            return jsonify({'status': 1, 'data': story_query.data}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to fetch story with given userid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

# * get all stories from category


@story_bp.route("/category/<string:category>", methods=['GET'])
def get_category_story(category):
    try:
        from app import Supabase  # * to avoid circular error
        # * fetch query
        story_query = Supabase.table('Story').select(
            "*",
            "User(*)"
        ).eq('category', category).eq('enabled', True).execute()

        if story_query.data:
            return jsonify({'status': 1, 'data': story_query.data}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to fetch story with given category'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

# * get all stories from author name or title of the story


@story_bp.route("/search/<string:searchterm>", methods=['GET'])
def get_search_story(searchterm):

    try:
        from app import Supabase  # * to avoid circular error

        # Build query
        story_query = Supabase.table("Story").select(
            "*",
            "User(*)"
        ).eq('enabled', True).ilike("title", f"%{searchterm}%")

        # Execute query
        results = story_query.execute()

        if results.data is not None:
            return jsonify({'status': 1, 'data': results.data}), 200
        else:
            return jsonify({'status': 0, 'message': 'No stories found'}), 500

    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500


# * to update story by storyid
# * cannot delete or change author


@story_bp.route("/<string:storyid>", methods=['PATCH'])
def update_story(storyid):
    from app import Supabase  # * to avoid circular error
    try:
        data = request.get_json() or {}

        # * Fetch query
        story_query = Supabase.table('Story').select(
            '*').eq('story_id', storyid).eq('enabled', True).execute()

        if not story_query.data:
            return jsonify({'status': 0, 'message': 'No record exists for given storyid'}), 400

        req_body = {}

        # * Update fields if they exist in data
        if 'title' in data:
            req_body['title'] = data['title']
        if 'description' in data:
            req_body['description'] = data['description']
        if 'category' in data:
            req_body['category'] = data['category']

        # * Handle imgurl
        if 'imgurl' in data:
            # current_imgurl = story_query.data[0].get('imgurl')
            # new_imgurl = data['imgurl']
            # index = len(current_imgurl) - 1
            new_entry = {'img': data['imgurl'], 'index': 0}
            # print('current_imgurl ', current_imgurl)
            req_body['imgurl'] = new_entry

        # * Handle liked_by
        # * if likedby already exists, then append to array
        # * else remove from array
        if 'liked_by' in data:
            liked_by = data['liked_by']
            current_liked_by = story_query.data[0].get(
                'liked_by', [])  # Initialize as empty list if None
            if current_liked_by is None:
                req_body['liked_by'] = [liked_by]
            elif liked_by in current_liked_by:
                current_liked_by.remove(liked_by)
                req_body['liked_by'] = current_liked_by
            else:
                current_liked_by.append(liked_by)
                req_body['liked_by'] = current_liked_by

        # * Update query
        update_query = Supabase.table('Story').update(
            req_body).eq('story_id', storyid).execute()

        if update_query.data:
            return jsonify({'status': 1, 'message': 'Successfully updated'}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to update story with given storyid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500


# * soft delete story from database


@story_bp.route("/<string:storyid>", methods=['DELETE'])
def delete_story(storyid):
    from app import Supabase  # * to avoid circular error
    try:

        # * delete query
        delete_query = Supabase.table('Story').update(
            {'enabled': False}).eq('story_id', storyid).execute()

        if delete_query.data:
            return jsonify({'status': 1, 'message': 'Successfully deleted'}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to delete story with given storyid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500


# * Text to speech recognition


@story_bp.route("/texttospeech", methods=['POST'])
def text_to_speech():
    try:
        client = OpenAI()
        data = request.get_json() or {}
        voice = 'alloy'

        if data['voice'] == 'male':
            voice = 'alloy'
        elif data['voice'] == 'female':
            voice = 'nova'
        elif data['voice'] == 'normal':
            voice = 'shimmer'

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=data['description']
        )
        # Open a file in binary mode to write the audio content
        with open("output.mp3", "wb") as file:
            # Write the response content to the file
            file.write(response.content)

        return send_file("../output.mp3", as_attachment=True), 200

    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

# * text to image generation


@story_bp.route("/texttoimage", methods=['POST'])
def text_to_image():
    try:
        client = OpenAI()
        data = request.get_json() or {}
        voice = 'alloy'

        response = client.images.generate(
            model="dall-e-3",
            prompt="a white siamese cat",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Open a file in binary mode to write the audio content
        return jsonify({'status': 1, 'data': response.data[0].url}), 200

    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

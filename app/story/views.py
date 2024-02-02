from flask import request, jsonify
from . import story_bp

# * input: userid, description, title, category, imgurl


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
            '*').eq('story_id', storyid).eq('enabled', True).execute()

        if story_query.data:
            return jsonify({'status': 1, 'data': story_query.data}), 200
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
            '*').eq('author', userid).eq('enabled', True).execute()

        if story_query.data:
            return jsonify({'status': 1, 'data': story_query.data}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to fetch story with given storyid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500


# * to update story by storyid
# * cannot delete or change author


@story_bp.route("/<string:storyid>", methods=['PATCH'])
def update_story(storyid):
    from app import Supabase  # * to avoid circular error
    try:
        data = request.get_json() or {}

        # Fetch query
        story_query = Supabase.table('Story').select(
            '*').eq('story_id', storyid).eq('enabled', True).execute()

        if not story_query.data:
            return jsonify({'status': 0, 'message': 'No record exists for given storyid'}), 400

        req_body = {}

        # Update fields if they exist in data
        if 'title' in data:
            req_body['title'] = data['title']
        if 'description' in data:
            req_body['description'] = data['description']
        if 'category' in data:
            req_body['category'] = data['category']

        # Handle imgurl
        if 'imgurl' in data:
            # current_imgurl = story_query.data[0].get('imgurl')
            # new_imgurl = data['imgurl']
            # index = len(current_imgurl) - 1
            new_entry = {'img': data['imgurl'], 'index': 0}
            # print('current_imgurl ', current_imgurl)
            req_body['imgurl'] = new_entry

        # Handle liked_by
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

        # Update query
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

        # delete query
        delete_query = Supabase.table('Story').update(
            {'enabled': False}).eq('story_id', storyid).execute()

        if delete_query.data:
            return jsonify({'status': 1, 'message': 'Successfully deleted'}), 200
        else:
            return jsonify({'status': 0, 'message': 'Failed to delete story with given storyid'}), 500
    except Exception as e:
        return jsonify({'status': 0, 'message': str(e)}), 500

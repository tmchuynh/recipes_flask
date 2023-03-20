from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date_made = data['date_made']
        self.description = data['description']
        self.instructions = data['instructions']
        self.if_under_30 = data['if_under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipe Join user on recipe.user_id = user.id"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_recipes = []
        if len(results) == 0:
            return list_of_recipes
        for result in results:
            list_of_recipes.append(result)
        return list_of_recipes
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipe WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        
        if not results:
            return None
        return Recipe(results[0])
    
    @classmethod
    def get_user_created(cls, data):
        query = "SELECT user.first_name FROM recipe JOIN user ON recipe.user_id = user.id WHERE recipe.id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if not result:
            return None
        return result[0]['first_name']
    
    @classmethod
    def create_recipe(cls, data):
        print("recipes", data)

        query = "INSERT INTO recipe (name, date_made, description, instructions, if_under_30, user_id) VALUES (%(name)s, %(date_made)s, %(description)s, %(instructions)s, %(if_under_30)s, %(user_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print("results", results)
        # if len(results) == 0:
        #     flash('Recipe not created')
        # else:
        #     flash('Recipe created')
        return results
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipe SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, if_under_30 = %(if_under_30)s WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) == 0:
            flash('Recipe not updated')
        else:
            flash('Recipe updated')
        return cls(results)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipe WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results == None:
            return "success"
        else:
            return "failure"
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        
        
        if len(recipe['name']) < 3:
            is_valid = False
            flash('Recipe name cannot be empty')
        if len(recipe['description']) <= 3:
            is_valid = False
            flash('Please enter a recipe with a description of at least 4 characters')
        if len(recipe['instructions']) <= 3:
            is_valid = False
            flash('Please enter a recipe with instructions of at least 4 characters')
        if recipe.get('if_under_30') is None:
            is_valid = False
            flash('Please mark whether the recipe takes more than 30 minutes')
        if len(recipe['date_made']) == 0:
            is_valid = False
            flash('Recipe date_made cannot be empty')
        return is_valid

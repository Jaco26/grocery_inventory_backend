from app.database.models import FoodKind, FoodItem, Stock

def delete_food_kind(kind_id='', user_id='', force=False):
  food_kind = FoodKind.query.get_or_404(kind_id)
  # do any FoodItems of this FoodKind exist in any stocks associated with this user?
  user_stocks = Stock.query.filter_by(user_id=user_id).all()

  food_items = []
  for stock in user_stocks:
    for item in stock.food_items:
      if item.food_kind_id == food_kind.id:
        food_items.append(item)
  
  if len(food_items) and not force:
    msg = '''You currently have stock items of kind "{}". 
If you continue, these items will be deleted as 
well. This action is irriversible'''.format(food_items[0].food_kind.name)
    return msg, 401
  
  if len(food_items) and force:
    for x in food_items:
      x.delete()
    
  food_kind.delete()

  return 'Ok', 200

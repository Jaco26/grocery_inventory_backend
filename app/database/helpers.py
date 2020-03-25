from app.database.models import FoodKind, StockItem, Stock

def delete_food_kind(kind_id='', user_id='', force=False):
  food_kind = FoodKind.query.get_or_404(kind_id)

  if food_kind.user_id != user_id:
    return 'You do not have permission to delete this "food kind"', 401
  # do any StockItems of this FoodKind exist in any stocks associated with this user?
  user_stocks = Stock.query.filter_by(user_id=user_id).all()

  stock_items = []
  for stock in user_stocks:
    for item in stock.stock_items:
      if item.food_kind_id == food_kind.id:
        stock_items.append(item)
  
  if len(stock_items) and not force:
    msg = '''You currently have stock items of kind "{}". 
If you continue, these items will be deleted as 
well. This action is irriversible'''.format(stock_items[0].food_kind.name)
    return msg, 401
  
  if len(stock_items) and force:
    for x in stock_items:
      x.delete()
    
  food_kind.delete()

  return 'Ok', 200

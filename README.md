# Concepts - Definition of Terms
Below are descriptions of key terms and concepts.

## User
A `user` has auth credentials used to log in and out of the app.
Each user can have one or more `stock`s.

## Stock
A `stock` represents a grouping of foodstuffs. Each user is free to define what exactly a `stock` in this app represents. For example, a user could create two stocks, one for the refrigerator and one for the pantry. Of course, using one stock to represent the entirety of a user's food innventory makes a lot of sense too (e.g. stock == food in house)

## Food Item
The base unit of qunatitative measure in the app. A `food_item` represents an amount of a specific `food_kind`. It includes information about how much of it there is, when it was new, and when it expires, what sort of packaging it has (if applicable), and the state of that packaging.

## Food Kind
The base unit of food categorization. Includes name, nutritional information, and optional user-defined notes about use and other miscellaneous considerations. Each `food_kind` can belong to multiple `food_category`s.

## Food Category
Used for high level organization––think food pyramid or other taxonomies. These are user defined tags used to categorize/organize/group food kinds; think, more granular, open source, 'food pyramid'.



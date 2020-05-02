# Patrick Johnson          5/1/2020 #
# SWDV 630 3W 20/SP2  Final Project #
#####################################
#Point of Sale System - Partial Implementation

# Classes
class Category:
    __next_id = 1
    
    def __init__(self, description):
        self.category_id = Category.__next_id
        Category.__next_id +=1
        self.description = description
        
    def __str__(self):
        return self.description

class Employee:
    __next_id = 1
    
    def __init__(self, name, PIN):
        self.employee_id = Employee.__next_id
        Employee.__next_id +=1
        self.name = name
        self.__PIN = PIN
       
    def __repr__(self):
        return "Employee - ID: {}; Name: {}".format(self.employee_id, self.name)
        
    def verify_PIN(self, PIN):
        return self.__PIN == PIN
    
    def update_PIN(self, old_PIN, new_PIN):
        if self.verify_PIN(old_PIN):
            self.__PIN = new_PIN
            return True
        else:
            return False
    
class Manager(Employee):
    pass

class Clerk(Employee):
    pass

class Item:
    __next_id = 1
    
    def __init__(self, barcode, description, category, employee):
        self.item_id = Item.__next_id
        Item.__next_id += 1
        self.barcode = barcode
        self.description = description
        self.category = category
        self.employee = employee
        
    def __repr__(self):
        return "Item - ID: {} Barcode: {}; Category: {}; Description: {}".format(self.item_id,
                                                                                self.barcode,
                                                                                self.category,
                                                                                self.description)
    
    def get_price(self):
        #pass
        return 5
        
    Total = property(get_price, None, None, "Item Price")

#   
#     @classmethod
#     def get_item_from_barcode(cls, barcode):
#         return Item(barcode, "Something", "Generic Category", "Employee")
#

class Fixed_Price_Item(Item):
    def __init__(self, barcode, description, category, employee, price):
        Item.__init__(self, barcode, description, category, employee)
        self.price = price
        
    def get_price():
        return self.price
    
class Per_Unit_Item(Item):
    def __init__(self, barcode, description, category, employee, price, unit):
        Item.__init__(self, barcode, description, category, employee)
        self.unit = unit
        self.unit_price = price
        
    def get_price():
        return self.unit_price
        
class SaleItem:
    __next_id = 1
    
    def __init__(self, barcode, quantity, sale):
        self.sale_item_id = SaleItem.__next_id
        SaleItem.__next_id += 1
        #self.item = Item.get_item_from_barcode(barcode)
        self.quantity = quantity
        self.sale = sale
    
    def __str__(self):
        return "{} - {} @ ${}".format(self.item.description,
                                      self.quantity,
                                      self.item.get_price())
    
if __name__ == "__main__":
    # Add Employees
    bob = Manager("Bob S.", "1234")
    ann = Clerk("Ann D.", "0000")

    print("Bob's employee_id:",bob.employee_id)
    print("Ann's employee_id:",ann.employee_id)

    # Check PINs:
    print("Check incorrect PIN for Bob:", bob.verify_PIN("1111"))
    print("Check correct PIN for Bob:  ", bob.verify_PIN("1234"))

    #Update PIN
    print("Updating Bob's PIN to '5309'")
    bob.update_PIN("1234", "5309")
    print("Check old PIN for Bob:", bob.verify_PIN("1234"))
    print("Check new PIN for Bob:", bob.verify_PIN("5309"))


    # Add a category
    paper_category = Category("Paper Products")

    # Create Some Items
    itemA = Item(2622977076,"Notebook",paper_category,ann)
    itemB = Item(5,"Something",1,bob)
    
    fpItem = Fixed_Price_Item(28, "Something Fixed", paper_category, bob, 5.99)
    puItem = Per_Unit_Item(4353, "Paper", paper_category, ann, 0.25, "Sheet")
    
    print("itemA:",itemA)
    print("itemB:",itemB)

    # Create some sale items:
    first_sale = None
    line_item_1 = SaleItem(2622977076, 1,first_sale)
    line_item_1.item = itemA
    line_item_2 = SaleItem(5,3, first_sale)
    
    print(line_item_1)
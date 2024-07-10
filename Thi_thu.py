import pandas as pd

class Node:
    def __init__(self, InvoiceNo, value, color="red"):
        self.InvoiceNo = InvoiceNo
        self.value = value
        self.color = color  # New nodes are always inserted as red
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0, None, color="black")  # Sentinel NIL node
        self.root = self.NIL

    def insert(self, InvoiceNo, value):
        new_node = Node(InvoiceNo, value)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = None
        self._insert(new_node)

    def _insert(self, new_node):
        node = self.root
        parent = None

        while node != self.NIL:
            parent = node
            if new_node.InvoiceNo < node.InvoiceNo:
                node = node.left
            else:
                node = node.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.InvoiceNo < parent.InvoiceNo:
            parent.left = new_node
        else:
            parent.right = new_node

        if new_node.parent is None:
            new_node.color = "black"
            return

        if new_node.parent.parent is None:
            return

        self._fix_insert(new_node)

    def _fix_insert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self._right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    def delete(self, InvoiceNo):
        self._delete_node_helper(self.root, InvoiceNo)

    def _delete_node_helper(self, node, InvoiceNo):
        z = self.NIL
        while node != self.NIL:
            if node.InvoiceNo == InvoiceNo:
                z = node

            if node.InvoiceNo <= InvoiceNo:
                node = node.right
            else:
                node = node.left

        if z == self.NIL:
            print("Couldn't find InvoiceNo in the tree")
            return 0

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._rb_transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self._left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self._right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self._right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self._left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    def _rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    def _get_max_value_node(self, node):
        current = node
        while current.right != self.NIL:
            current = current.right
        return current


    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, InvoiceNo):
        return self._search_tree_helper(self.root, InvoiceNo)

    def _search_tree_helper(self, node, InvoiceNo):
        if node == self.NIL or InvoiceNo == node.InvoiceNo:
            return node

        if InvoiceNo < node.InvoiceNo:
            return self._search_tree_helper(node.left, InvoiceNo)
        return self._search_tree_helper(node.right, InvoiceNo)

    def asorder(self):
        return self._asorder(self.root)

    def _asorder(self, node):
        result = []
        if node != self.NIL:
            result = self._asorder(node.left)
            result.append((node.InvoiceNo, node.value))
            result = result + self._asorder(node.right)
        return result

    def desorder(self):
        return self._desorder(self.root)

    def _desorder(self, node):
        result = []
        if node != self.NIL:
            result = self._desorder(node.right)
            result.append((node.InvoiceNo, node.value))
            result = result + self._desorder(node.left)
        return result

    def delete_leftmost_node(self):
        if self.root != self.NIL:
            self.root = self._delete_leftmost_node(self.root)

    def _delete_leftmost_node(self, node):
        if node.left == self.NIL:
            return node.right
        node.left = self._delete_leftmost_node(node.left)
        return node

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node == self.NIL:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return max(left_height, right_height) + 1

    def filter_buyers(self, country):
        return self._filter_buyers(self.root, country)

    def _filter_buyers(self, node, country):
        filtered = []
        if node != self.NIL:
            filtered += self._filter_buyers(node.left, country)
            if node.value["Country"] == country:
                filtered.append((node.InvoiceNo, node.value))
            filtered += self._filter_buyers(node.right, country)
        return filtered

    def save_to_csv(self, file_path):
        data = self.asorder()
        formatted_data = [(InvoiceNo, value["Name"], value["Age"]) for InvoiceNo, value in data]
        df = pd.DataFrame(formatted_data, columns=['InvoiceNo', 'Name', 'Age'])
        df.to_csv(file_path, index=False)
        print(f"Tree saved to {file_path}")

def read_csv_to_rbt(data_path, rbt):
    df = pd.read_csv(data_path)
    df = df[:1000]
    for _, row in df.iterrows():
        InvoiceNo = str(row['InvoiceNo'])
        # StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
        value = {
            "StockCode": str(row["StockCode"]),
            "Description": str(row["Description"]),
            "Quantity": str(row["Quantity"]),
            "InvoiceDate": str(row["InvoiceDate"]),
            "UnitPrice": str(row["UnitPrice"]),
            "CustomerID": str(row["CustomerID"]),
            "Country": str(row["Country"]),
        }
        rbt.insert(InvoiceNo, value)


if __name__ == "__main__":
    rbt = RedBlackTree()
    data_path = "D:\Workspace\Python code\Data\OnlineRetail.csv"
    read_csv_to_rbt(data_path, rbt)
    while True:
        # try:
            print()
            print("Menu")
            print("0. Quit")
            print("1. Insert")
            print("2. Delete")
            print("3. Search")
            print("4. Ascending-order")
            print("5. Descending-order")
            print("6. Min InvoiceNo-node")
            print("7. Max InvoiceNo-node")
            print("8. buyer-list, whose age less than 25")
            print("9. Delete right-most node")
            print("10. Save to CSV file")
            print("11. Delete left-most node")
            print("12. Height of the tree")
            print("13. Filter buyers")
            
            print()
            n = int(input("Your choice: "))
            print()
            if n == 0:
                print("Exiting...")
                break
            elif n == 1:
                InvoiceNo = str(input("InvoiceNo: "))
                StockCode = str(input("StockCode: "))
                Description = str(input("Description: "))
                Quantity = str(input("Quantity: "))
                InvoiceDate = str(input("InvoiceDate: "))
                UnitPrice = str(input("UnitPrice: "))
                CustomerID = str(input("CustomerID: "))
                Country = str(input("Country: "))
                value = {
                    "StockCode": StockCode,
                    "Description": Description,
                    "Quantity": Quantity,
                    "InvoiceDate": InvoiceDate,
                    "UnitPrice": UnitPrice,
                    "CustomerID": CustomerID,
                    "Country": Country,
                }
                rbt.insert(InvoiceNo, value)
                print()
                print("Insert operation DONE!")
            elif n == 2:
                result = rbt.delete(str(input("InvoiceNo: ")))
                if result:
                    print('Delete Done!')
                print()
            elif n == 3:
                search_InvoiceNo = str(input("InvoiceNo: "))
                result = rbt.search(search_InvoiceNo)
                if result != rbt.NIL:
                    print(f"Found {search_InvoiceNo} in the RBT with value: {result.value}")
                else:
                    print(f"{search_InvoiceNo} is not in the RBT.")
            elif n == 4:
                print("Ascending-order traversal of the RBT: ", rbt.asorder())
            elif n == 5:
                print("Descending-order traversal of the RBT: ", rbt.desorder())
            elif n == 6:
                min_node = rbt._minimum(rbt.root)
                print(f"The minimum value node in the RBT is {min_node.InvoiceNo} with value: {min_node.value}")
            elif n == 7:
                max_node = rbt._get_max_value_node(rbt.root)
                print(f"The maximum value node in the RBT is {max_node.InvoiceNo} with value: {max_node.value}")
            elif n == 8:
                buyers = rbt.asorder()
                young_buyers = [buyer for buyer in buyers if buyer[1]['Age'] < 25]
                name_young_buyers = [buyer[1]['Name'] for buyer in young_buyers]
                count = len(name_young_buyers)
                print(f"Number of buyers, whose age is less than 25 is {count}, including: ", name_young_buyers)
            elif n == 9:
                max_node = rbt._get_max_value_node(rbt.root)
                rbt.delete(max_node.InvoiceNo)
                print("Delete right-most node DONE!")
            elif n == 10:
                data_path_save = "D:/Workspace/Data/buyer_data.csv"
                rbt.save_to_csv(data_path_save)
            elif n == 11:
                rbt.delete_leftmost_node()
                print("Delete left-most node DONE!")
            elif n == 12:
                height = rbt.height()
                print(f"The height of the tree is: {height}")
            elif n == 13:
                filtered_buyers = rbt.filter_buyers('United Kingdom')
                for buyer in filtered_buyers:
                    print(f"InvoiceNo: {buyer[1]['CustomerID']}")
            elif n == 14:
                results = rbt.asorder()
                min_quantity = 10000000000
                for result in results:
                    # print(result[1]['Quantity'])
                    if min_quantity > int(result[1]['Quantity']):
                        min_quantity = int(result[1]['Quantity'])
                        min_InvoiceNo = result[0]
                print(f'Min quantity: {min_quantity} for InvoiceNo: {min_InvoiceNo}')

            else:
                print("Please input your choice from 0 to 13")
        # except Exception as e:
        #     print()
        #     print(f"Please input integer! Error: {e}")


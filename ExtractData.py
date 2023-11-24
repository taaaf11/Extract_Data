import json

class ExtractData:
    """
    Extracting data from a file and converting it into python-code usable format.
      -> Dictionary
      -> List
      -> Tuple
      
    Also:
      -> JSON

    -> Class for handling different methods of data extraction.
    """
    def __init__(self, file_name: str, mode: str, separator: str, trim_newline: bool) -> None:
        self.fd = open(file_name, mode)
        self.separator = separator
        self.trim_newline = trim_newline # remove the trailing newline character at the end of the
                # last item of the line, if the item is included
        
        self.json_indent = None # this variable is used cz problems occur when specified as parameter
                    # in as_json() function
        
        self.lines_skipped = None # skip lines in range while reading file
    
    def skip_lines(self, line_range: str) -> None:
        """
        Skip lines while reading file
        
        SYNOPSIS:
            -> Skip a single line
                skip_lines('2-2')
            
            => Skip line no 2
            
            -> Skip lines in range
                skip_lines('1-5')
            
            => Skip lines 1 to 5
        """
        
        split_ed = line_range.split('-') # "6-9" becomes ['6', '9']
        self.lines_skipped = [int(i) for i in split_ed] # ['6', '9'] becomes [6, 9]

    # to be used inside the class
    # separates file data into lines
    def _into_lines(self) -> list:
        """
        Converts each line of the file to an item in the list.
        This list is returned.
        """
        eof = False
        lines = list()

        # read file
        while not eof:
            line = self.fd.readline()
            if not line:
                eof = True
            if line == '\n': # line is empty
                continue
            lines.append(line)
        
        # using del keyword to delete list items is a pain...
        # instead, initialize the list item with empty string
        # then filter that list
        if not (self.lines_skipped is None):
            for line_number in range(self.lines_skipped[0] - 1, self.lines_skipped[1]):
                lines[line_number] = ''
        
        # Filtering the list
        lines = [line for line in lines if not line == '']
                
        # reset the pointer to the start of the file in case of further function calls
        self.fd.seek(0)
        
        if lines[-1] == '':
            lines.pop()

        return lines
    
    @staticmethod
    def _square_to_braces_json(squary_json_data: str) -> str:
        """
        Change square brackets to braces in json data, at the start and at the end, as a string
        See comments in the as_json function
        """
        
        braces_json_data = list(squary_json_data)
        braces_json_data[0], braces_json_data[-1] = '{', '}'
        braces_json_data = ''.join(braces_json_data)
        
        return braces_json_data
    
    @staticmethod
    def _prep_dicts(list1: list, list2: list) -> list:
        """
        Prepare a dictionary for json in as_json method defined below
        It outputs a list with dictionaries in it. Example:
        
        list1 = ["Name", "Food", "Age"]
        list2  = [["Altaaf", "Brownies", "18"], ["Doe", "Burger", "45"]]
        
        _prep_dicts(list1,list2) :
        
        [{'Name': 'Altaaf', 'Food': 'Brownies', 'Age': '18'},
                {'Name': 'Doe', 'Food': 'Burger', 'Age': '45'}]
        """
        
        save_list = list()
        
        a_dict = {}
        for list_ in list2:
            for item in list1:
                a_dict.update({item: list_[list1.index(item)]})
            save_list.append(a_dict)
            a_dict = {}
        
        return save_list
    
    def as_dicts(self, keys: list, *values) -> list:
        """
        SYNOPSIS: 
            obj.as_dict(key: int, *values)
            
        EXAMPLE:
            Suppose file data is:
              
            1,Altaaf,18,Programmer,Traveller,Pizza
            2,David,36,Engineer,Gardener,Berries
            
            -> obj.as_dict(["Name"], 2)
            
            ==> [{'Name': 'Altaaf'}, {'Name': 'David'}]
            
                                                OR
            
            obj.as_dict(["Name", "Age"], 2, 3)
            
            ==> [{'Name': 'Altaaf', 'Age': '18'}, {'Name': 'David', 'Age': '36'}]
        """
        
        save_datas = list()
        hold_dicts = list()
        
        for line in self._into_lines():
            split_ed = line.split(self.separator)
            list_values = list()

            for value in values:
                list_values.append(split_ed[value-1])
            
            if (self.trim_newline):
                for list_value in list_values:
                    
                     # as the line item containing '\n' will be in the last item of the line
                     # no need of any further filtering
                    if list_value[-1] == '\n':
                        list_values.append(list_value[:-1])
                        list_values.remove(list_value)
            
            save_datas.append(list_values)
        
        hold_dicts = self._prep_dicts(keys, save_datas)

        return hold_dicts

    def as_list(self, item_num: int) -> list:
        """
        SYNOPSIS:
            obj.as_list(item_num)
            
            -> Returns a list with item_num-th item from delimited line.
            -> This happens with all lines in given file.
        
        EXAMPLE:
            obj.as_list(3)
            
            -> Add third item from each line of the given file
        """
        list_ = list()

        for line in self._into_lines():
            split_ed = line.split(self.separator)
            list_.append(split_ed[item_num-1])

        return list_

    def as_tuple(self, item_num: int) -> tuple:
        """
        SYNOPSIS:
              obj.as_list(item_num)

              -> Returns a list with item_num-th item from delimited line.
              -> This happens with all lines in given file.

        EXAMPLE:
              obj.as_list(3)

              -> Add third item from each line of the given file
        """
        
        return tuple(self.as_list(item_num))
    
    def set_json_indent(self, indent_level: int) -> None:
        """
        Set json indent
        """
        self.json_indent = indent_level
    
    def as_json(self, fields: list, *values) -> str:
        """
        SYNOPSIS:
              obj.as_json(fields, *vales)
              
              -> The length of list should be equal to the length of asked items,
                for establishing one-to-one correspondance for json fields and values
            
              -> Adds to json data such that:
                => Elements in the list appear as json fields
                => Asked item numbers appear as json values
            
              -> Returns a string of json data
        
        EXAMPLE:
              Suppose file data is:
              
              1,Altaaf,18,Programmer,Traveller,Pizza
              2,David,36,Engineer,Gardener,Berries
              
              -> obj.as_json(["Name", "Age"], 2, 3)
              
              => Returns:
                  {
                      {
                          "Name":  "Altaaf"
                          "Age":  "18"
                      },
                      {
                          "Name":  "David
                          "Age":  "36"
                      }
                  }
                  
              -> obj.as_json(["Name"], 2)
              
              => Returns:
                  {
                      {
                          "Name":  "Altaaf"
                      },
                      {
                          "Name":  "David"
                      }
                  }
                  
              Note that this pretty printing is optional, and can be set be function
              obj.set_json_indent(indent_level)
        """
        
        save_datas = list()
        hold_dicts = list()
        
        for line in self._into_lines():
            split_ed = line.split(self.separator)
            list_values = list()

            for value in values:
                list_values.append(split_ed[value-1])
            
            if (self.trim_newline):
                for list_value in list_values:
                    
                     # as the line item containing '\n' will be in the last item of the line
                     # no need of any further filtering
                    if list_value[-1] == '\n':
                        list_values.append(list_value[:-1])
                        list_values.remove(list_value)
            
            save_datas.append(list_values)
                
        hold_dicts = self._prep_dicts(fields, save_datas)

        # As hold_dicts variable is a list, we don't want square brackets in the start and at the end of
        # our data
        # Without replacing, data appears as:
        
        # [
        #    {
        #       ...
        #    }
        # ]
        
        # So, the solution is to replace the first and the last "character" of the data,
        # obviously, as a string
        # self._square_to_braces_json method does that for us
        
        if not (self.json_indent is None): # Indent level, self.json_indent can be set by set_json_indent method
            prettier_json_data = json.dumps(hold_dicts, indent=self.json_indent)
            prettier_json_data = self._square_to_braces_json(prettier_json_data)
            return prettier_json_data
        
        else:
            json_data = json.dumps(hold_dicts)
            json_data = self._square_to_braces_json(json_data)
            return json_data
    
    def close_(self) -> None:
        """
        Close the opened file in object instantiation
        """
        self.fd.close()
    
    def __eq__(self, other) -> bool:
        return (self.fd == other.fd)
    
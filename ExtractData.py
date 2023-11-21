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
    def __init__(self, file_name, mode: str, separator: str, trim_newline: bool) -> None:
        self.fd = open(file_name, mode)
        self.separator = separator
        self.trim_newline = trim_newline # remove the trailing newline character at the end of the
                # last item of the line, if the item is included
        
        self.json_indent = None # this variable is used cz problems occur when specified as parameter
                    # in as_json() function

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
        
        # reset the pointer to the start of the file in case of further function calls
        self.fd.seek(0)
        
        if lines[-1] == '':
            lines.pop()

        return lines
    
    def as_dict(self, key: int, *values) -> dict:
        """
        SYNOPSIS: 
            obj.as_dict(key: int, *values)
            
        EXAMPLE:
            obj.as_dict(1, 2)
            
            Add first item of every line as a key and second as value in the dictionary.
            
                                                OR
            
            obj.as_dict(1, '2-3')
            
            Add first item of every line as a key and second-third item as values in the dictionary.
            Added as a list
        """
        
        dictionary = dict()

        for line in self._into_lines():
            split_ed = line.split(self.separator)
            dict_values = list()

            for value in values:
                if isinstance(value, str) and '-' in value: # range
                    dict_values.append(split_ed[int(value.split('-')[0])-1: int(value.split('-')[1])])
                    continue
                dict_values.append(split_ed[value-1])
            
            if (self.trim_newline):
                for dict_value in dict_values[0]:
                    
                     # as the line item containing '\n' will be in the last item of the line
                     # no need of any further filtering
                    if dict_value[-1] == '\n':
                        dict_values[0].append(dict_value[:-1])
                        dict_values[0].remove(dict_value)

            if len(dict_values) == 1:
                dictionary.update({split_ed[key-1]: dict_values[0]})

            else:
                dictionary.update({split_ed[key-1]: dict_values})

        return dictionary

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
    
    def as_json(self, key: int, *values):
        """
        SYNOPSIS: 
            obj.as_json(key: int, *values)
            
        EXAMPLE:
            obj.as_json(1, 2)
            
            Add first item of every line as a field and second as value in the value.
            
                                                OR
            
            obj.as_json(1, '2-3')
            
            Add first item of every line as a field and second and third item as values in the json value.
            Added as list.
        """
        
        # indenation is controlled by self.json_indent variable
        if not (self.json_indent is None):
            return json.dumps(self.as_dict(key, *values), indent=self.json_indent)
        
        else:
            return json.dumps(self.as_dict(key, *values))
    
    def close_(self) -> None:
        """
        Close the opened file in object instantiation
        """
        self.fd.close()
    
    def __eq__(self, __value: object) -> bool:
        return (self.file == __value.file) and (self.mode == __value.mode)
    
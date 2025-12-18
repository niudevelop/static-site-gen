class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = ""
        if self.props is None or self.props == False:
            return props
        for k,v in self.props.items():
            props += f' {k}="{v}"'
        return props
    
    def __repr__(self):
        result = f"<{self.tag}{self.props_to_html()}>"
        if self.children is not None and len(self.children) > 0:
            for child in self.children:
                result += "\n" + repr(child)
        if self.value is not None:
            result += f"{self.value}"
        result += f"</{self.tag}>"
                
        return result
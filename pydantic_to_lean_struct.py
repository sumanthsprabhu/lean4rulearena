#"vibe" coded; doesn't support other structure yet (like List[Student])
from structured_forms import Student, Form1040
from typing import get_args, get_origin, List, Optional, Union

def python_type_to_lean(py_type):
    origin = get_origin(py_type)
    if origin == list or origin == List:
        inner_type = get_args(py_type)[0]
        return f"List {python_type_to_lean(inner_type)}"
    elif origin == Optional or origin == Union:
        inner_type = [t for t in get_args(py_type) if t is not type(None)][0]
        return f"Option {python_type_to_lean(inner_type)}"
    elif isinstance(py_type, type):
        mapping = {
            str: "String",
            int: "Int",
            float: "Float",
            bool: "Bool",
        }
        return mapping.get(py_type, py_type.__name__)
    else:
        return "String"


def pydantic_to_lean_struct(model, seen=None):
    if seen is None:
        seen = set()
    lines = []
    if model.__name__ in seen:
        return ""
    for field_info in model.model_fields.values():
        annotation = field_info.annotation
        origin = get_origin(annotation)
        if origin == list or origin == List:
            inner = get_args(annotation)[0]
            if isinstance(inner, type) and issubclass(inner, BaseModel):
                lines.append(pydantic_to_lean_struct(inner, seen))
            elif isinstance(annotation, type) and issubclass(annotation, BaseModel):
                lines.append(pydantic_to_lean_struct(annotation, seen))
                
    struct_lines = [f"structure {model.__name__} where"]
    
    for name, field in model.model_fields.items():
        desc = f"--{field.description}" if field.description else ""
        lean_type = python_type_to_lean(field.annotation)
        struct_lines.append(f"{desc}")
        struct_lines.append(f"{name} : {lean_type}")

    lines.append("\n".join(struct_lines))

    return "\n\n".join(lines)


if __name__ == "__main__":
    lean_struct = pydantic_to_lean_struct(Form1040)
    print(lean_struct)



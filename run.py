from parent import Parent

def main():

    parent = Parent(2)
    other_parent = Parent(2)
    parent.add(other_parent)
    print parent.content()

if __name__ == "__main__":
    main()

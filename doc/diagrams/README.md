## Generating plantuml files

For generating images from source UML diagram files (in plantuml format),
see https://hub.docker.com/r/think/plantuml/.

    cat mydiagram.plantuml | docker run --rm -i think/plantuml -tpng > mydiagram.png



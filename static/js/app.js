function visualizarFoto(evento){
    const files = evento.target.files
    const archivo = files [0]
    const objectURL = URL.createObjectURL(archivo)
    imagenProducto.setAttribute("src",objectURL)
}

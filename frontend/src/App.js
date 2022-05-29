import { useCallback, useEffect, useRef, useState } from 'react';
import {  Navbar, Container,Nav, Button } from 'react-bootstrap'
import './App.css';

function App() {
  const inputRef = useRef(), outputRef = useRef();
  const [hasImg, setHasImg] = useState(false);

  // 
  const canvasRef = useRef(null);
  useEffect(() => {
    let c = canvasRef.current = document.createElement("canvas");
    canvasRef.current.ctx = c.getContext("2d");
  }, []);

  // 
  const onInputLoad = (img) => {
    const canvas = canvasRef.current, ctx = canvas.ctx;
    canvas.width = canvas.height = 256;

    console.dir(img)
  
    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight, 0, 0, 256, 256);

    setHasImg(true);
    let data, xhr;

    data = new FormData();
    data.append("base64", canvas.toDataURL());

    xhr = new XMLHttpRequest();

    xhr.open("POST", "http://localhost:5000/process", true);

    xhr.onreadystatechange = function ( response ) {
      outputRef.current.src = response.target.responseText.replace(/-/g, "+").replace(/_/g, "/");
      console.log(response)
    };
    xhr.send(data);
  };
  
  // 
  const onOpenFile = useCallback((file) => {
    let input = file.target;
    let reader = new FileReader();
    reader.onload = () => {
      let dataURL = reader.result;
      let input = inputRef.current;
      input.onload = () => {
        onInputLoad(input);
        input.onload = null;
      };
      input.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
  }, []);

  // 
  const onReset = useCallback(() => {
    inputRef.current.src = outputRef.current.src = "";
    setHasImg(false);
  }, []);

  // 
  return (
    
      <div className="app">
          <Navbar bg="primary" variant="dark">
            <Container>
            <Navbar.Brand>Capstone Demo - Grayscale image colorized using DNN</Navbar.Brand>
            <Nav className="me-auto">
              <Nav.Link href="https://github.com/CedricHwong/Cloud-Deployment-of-Deep-Learning-Networks">GitHub</Nav.Link>
              <Nav.Link href="https://www.kaggle.com/datasets/theblackmamba31/landscape-image-colorization">Dataset</Nav.Link>
              <Nav.Link href="https://drive.google.com/drive/folders/1PcVYKDo8j1vo72hNtUtYSFK3dvCKr9cl?usp=sharing">Pre-trained Model</Nav.Link>
              <Nav.Link href="/">Youtube</Nav.Link>
            </Nav>
            </Container>
          </Navbar>

        <div className='img-wrapper'><img alt="" ref={inputRef} /></div>
        <div className='btns'>
          {hasImg
          ? <Button variant="primary" onClick={onReset}>Reset</Button>
          // : <input type="file" accept="image/*" onChange={onOpenFile} />
          : <>
            <label class="form-label" for="customFile">Colorize black and white images using the image colorization API. Add color to old family photos and historic images, and bring them back to life with colorization.</label>
            <input type="file" class="form-control" id="customFile" accept="image/*" onChange={onOpenFile} />
            </>
          }
        </div>
        <div className='img-wrapper'><img alt="" ref={outputRef} /></div>
      </div>
  );
}



// 
export default App;

import React, {Component} from 'react';
import axios from 'axios';

class ImageWidget extends Component{
    state = {
        file: "",
        fileObj: null,
        uploaded: false
    }


    handler = (evt) =>{
        const filename = evt.target.value;
        if(filename.includes('.png') || filename.includes('jpg')){
            let reader = new FileReader();
            reader.onload = (e) => {
                this.setState({
                    fileObj: e.target.result,
                    file: filename,
                    uploaded: false
                })
            }
            reader.readAsDataURL(evt.target.files[0]);

        }else{
            alert('Please select a file with the extentions .png or .jpg');
        }
    }

    uploadHandler = () =>{
        const token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        console.log(token);
        console.log(this.state.file);
        axios({
            method: 'GETT',
            url: '/api/image-upload',
            data: {
                
                'filename': this.state.file
            }
        })
    }
    render(){
        let renderedHTML = null;
        console.log(this.state.file);
        if(this.state.file === ""){
            renderedHTML = 
            (<div>
                <h3>No Image file selected</h3>
                <h6>Choose one from the file system</h6>
                <input 
                    className="btn"
                    type="file"
                    value={this.state.file}
                    onChange={this.handler}/>
            </div>);
        }else{
            renderedHTML = 
                <div>
                    <h3>File Selected For Printing</h3>
                    <img 
                        className="img-thumbnail"
                        src={this.state.fileObj} /><br />
                    <h6>Send to server for analysis</h6>
                <form encType="multipart/form-data" method="POST" action="/api/image-upload">
                    <input 
                        name="image"
                        type="file"
                        onChange={this.handler}/>
                    <input 
                        className="btn btn-primary"
                        type="submit" value="Upload" />
                </form>
                </div>    
        }
        const withFile = (<div>
                        <h3>File Selected For Printing</h3>
                            <img 
                                className="img-thumbnail"
                                src={this.state.fileObj} /><br />
                            <h6>Send to server for analysis</h6>
                        </div>
                            );
        const withoutFile = (
            <div>
                <h3>No Image file selected</h3>
                <h6>Choose one from the file system</h6>
            </div>
        );
        return(
            <div className="well">
                <div>
                    { this.state.file === "" 
                    ? withoutFile 
                    : withFile
                    } 
                    <form encType="multipart/form-data" method="POST" action="/api/image-upload">
                    <input 
                        name="image"
                        type="file"
                        onChange={this.handler}/>
                    <input 
                        className="btn btn-primary"
                        type="submit" value="Upload" />
                </form>
                </div>
            </div>
        );
    }
}


export default ImageWidget;
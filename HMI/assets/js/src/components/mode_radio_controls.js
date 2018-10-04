import React from 'react';

const radioControls = (props) =>{
    return(
        <div>
        <h4>Mode</h4>
        <div onChange={props.handler}>
            <label >
            <input 
                type="radio" 
                className="form-control" 
                name="mode" 
                value="auto"
                 />Auto</label><br />
        <label >
            <input 
                type="radio" 
                className="form-control" 
                name="mode" 
                value="manual"/>Manual</label>
            </div>
            
        </div>
    )
}

export default radioControls
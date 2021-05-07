import React, { Component } from 'react';
import S3FileUpload from 'react-s3';

const config ={
  bucketName: "cmpe286",
  region:"us-east-1",
  accessKeyId:"AKIAVFQCFDNP2J7OEYOA",
  secretAccessKey:"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",
}

class App extends Component {
  upload=(event)=>{
    S3FileUpload.uploadFile(event.target.files[0], config)
    .then((data)=> {
      console.log(data.location)
    })
    .catch((err)=>{
      alert(err)
    })
  }
  render(){
    return (
      <div>
        <h3>Upload An Image</h3>
        <input type="file" onChange={this.upload}/>
      </div>
    );
  }
}

export default App;

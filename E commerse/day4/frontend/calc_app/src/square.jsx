import { useState } from "react"; 
 
export default function Square() { 
   const [num, setNum] = useState(0); 
   const[sqr,setSqr] = useState(0); 
   return ( 
    <> 
      <p>Number:<input type="text"  
      value={num} onChange={(e) => setNum(Number(e.target.value))} /></p> 
      <p><button onClick={() => setSqr(num * num)}>Calculate</button></p> 
      <p>Square of {num} is {sqr}</p> 
    </> 
  )
}
import styles from "../style";
import Navbar from './Navbar';
import { arrRight } from "../assets";

import { useEffect, useRef, useState } from "react";

export const Chat = () => {
  
  const textAreaRef = useRef(null);
  const [val, setVal] = useState("");
  const handleChange = (e) =>{
    setVal(e.target.value);
  }
  
  useEffect(() => {
    textAreaRef.current.style.height = "auto";
    textAreaRef.current.style.height = textAreaRef.current.scrollHeight + "px";
  }, [val])
  return(
  <section id="chat" className={`h-full flex flex-1 flex-col relative`}>
    <Navbar children={"chat-nav"}/>
    <div className="">
      <div></div>
      <div></div>
    </div>
    
    <div className={`${styles.flexCenter} flex-col fixed bottom-0 left-0 right-0 p-4`}>
      <label className={`${styles.flexBetween} flex-wrap w-[580px] p-3 max-h-[120px] mt-auto border-[2px] rounded-[17px] border-text_color overflow-y-auto overflow-x-hidden`}>
          <textarea placeholder="Enter your prompt" className={`${styles.grayMedium} w-full
          bg-transparent resize-none outline-none text-[18px] max-w-[520px]`} value={val} onChange={handleChange} rows={"1"} ref={textAreaRef}></textarea>
          <button className={`${styles.flexJustifyEnd} cursor-pointer`}>
            <img src={arrRight} alt="arr_right" className="w-[25px] fixed"/>
          </button>
      </label>
      <p className={`${styles.grayMedium} mt-3 text-[12px]`}>
        Explorer can make mistakes. Consider checking important information
      </p>
    </div>
  </section>
  )
}

export default Chat;
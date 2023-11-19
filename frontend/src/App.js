import styles from "./style";
import { Menu, Chat, Info } from "./components";

const App = () => (
  <div className="bg-primary w-full overflow-hidden relative">

    <div className={`${styles.flexStart}`}>
      <div className={`${styles.boxWidthSmall}`}>
        <Menu/>
      </div>
      <main className={`${styles.boxWidth}`}>
        <Chat />
      </main>
      <div className={`${styles.boxWidthSmall}`}>
        <Info />
      </div>
    </div>

  </div>
)

export default App;

import ReactHabitat from "react-habitat";

import BlastJob from "./components/blast_result";

class App extends ReactHabitat.Bootstrapper {
    constructor() {
        super();

        const builder = new ReactHabitat.ContainerBuilder();
        builder.register(BlastJob).as("BlastJob");
        this.setContainer(builder.build());
    }
}

export default new App();

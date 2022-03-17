import { observer } from "mobx-react";
import {Form, Modal, Message} from "semantic-ui-react";
import ReactTable from "react-table-6";
import BlastStore from "../stores/blast_store"
import _ from 'lodash';
import React from "react";

import ReactGA from 'react-ga';


@observer
export default class BlastJob extends React.Component {
    constructor(props) {
        super(props);
        this.store = new BlastStore();
    }

    componentDidMount() {
        this.store.loadBlastResults().then();
    }

    updateQuery = e => {
        if (e.target.value.match("^[CAGTcagt]+$")) {
            let blastJobData = this.getValue("blastJobData");
            this.store.setValue("isValidQuery", true)
            blastJobData["query"] = e.target.value;
            this.store.setValue("blastJobData", blastJobData)
        } else {
            this.store.setValue("isValidQuery", false)
        }
    }

    render() {
        let blastResults = this.store.getValue("blastResults");
        const columns = [
            {Header: "Result No", id: "result_no", accessor: "result_no"},
            {Header: "Seq Start", id: "sstart", accessor: "sstart"},
            {Header: "Seq End", id: "ssend", accessor: "ssend"},
            {Header: "Seq Strand", id: "sstrand", accessor: "sstrand"},
            {Header: "Evalue", id: "evalue", accessor: "evalue"},
            {Header: "Pident", id: "pident", accessor: "pident"},
            {Header: "Sequence", id: "sequence", accessor: "sequence"},
        ];

        return (
            <div style={{position: "relative"}}>
                <div>
                    <Form>
                        <TextArea
                            label="Query"
                            placeholder="CTAGATCA..."
                            onChange={this.updateQuery}
                            required
                            info={"Enter a value to run against BLAST"}
                        />
                        <Message
                            error
                            content={"Must be valid DNA sequence ('ACGT') "}
                            hidden={this.store.getValue("isValidQuery")}
                        />
                        <Form.Button
                            disabled={!this.store.getValue("isValidQuery")}
                            onClick={() => {
                                this.store.onSubmitBlastJob().then()
                            }}
                        >
                            Submit
                        </Form.Button>
                    </Form>
                </div>
                <div>
                    <ReactTable
                        data={blastResults}
                        hidden={_.isEmpty(blastResults)}
                        columns={columns}
                    />
                </div>
            </div>
        )
    }
}

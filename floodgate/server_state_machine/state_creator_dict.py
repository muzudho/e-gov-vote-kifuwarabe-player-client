from floodgate.server_state_machine.layer2_decoration_event.judgement import create as create_judgement
from floodgate.server_state_machine.layer2_decoration_event.match import create as create_match
from floodgate.server_state_machine.layer2_decoration_event.receipt import create as create_receipt
from floodgate.server_state_machine.layer2_decoration_event.tell import create as create_tell
from floodgate.keywords import JUDGEMENT, MATCH, RECEIPT, TELL

state_creator_dict = {
    JUDGEMENT: create_judgement,
    MATCH: create_match,
    RECEIPT: create_receipt,
    TELL: create_tell,
}

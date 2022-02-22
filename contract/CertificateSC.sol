// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract CertificateSC {
    address payable public owner;

    struct Transcript {
        bytes32 transcript;
        uint256 Timestamp;
    }

    event IsSuccess(bool value);

    constructor() payable {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    mapping(bytes32 => Transcript[]) private studentToTranscript;

    function is_transcript_exist(
        bytes32 hash_data,
        Transcript[] memory arrayTranscript
    ) private pure returns (bool) {
        for (uint256 i = 0; i < arrayTranscript.length; i++) {
            if (arrayTranscript[i].transcript == hash_data) {
                return true;
            }
        }
        return false;
    }

    function register_transcript(bytes32 transcriptHash, bytes32 studentId)
        public
        onlyOwner
        returns (bool success)
    {
        if (
            is_transcript_exist(transcriptHash, studentToTranscript[studentId])
        ) {
            emit IsSuccess(false);
            return false;
        } else {
            studentToTranscript[studentId].push(
                Transcript(transcriptHash, block.timestamp)
            );
            emit IsSuccess(true);
            return true;
        }
    }

    function retrieve_student_transcript(bytes32 studentId)
        public
        view
        onlyOwner
        returns (Transcript[] memory)
    {
        return studentToTranscript[studentId];
    }

    function verify_certificate_transcript(
        bytes32 transcriptHash,
        bytes32 studentId
    ) public view returns (bool) {
        bool transcriptExist = is_transcript_exist(
            transcriptHash,
            studentToTranscript[studentId]
        );
        return transcriptExist;
    }
}

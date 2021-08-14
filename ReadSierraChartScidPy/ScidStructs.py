# This is the Sierra Chart Intraday header file as defined in IntradayRecord.h
# It is 56 bytes long

from struct import *
import struct

#struct s_IntradayFileHeader
#{
#	static const uint32_t UNIQUE_HEADER_ID = 0x44494353;  // "SCID"
#	uint32_t FileTypeUniqueHeaderID;  // "SCID"
#	uint32_t HeaderSize;
#	uint32_t RecordSize;
#	uint16_t Version;
#	uint16_t Unused1;
#	uint32_t Unused2;
#	char Reserve[36];
#}
ifh_format = 'IIIHHI36s'
ifh_len = struct.calcsize(ifh_format)

#struct s_IntradayRecord
#{
#	SCDateTimeMS DateTime; // UInt64 microseconds since 12/30/1899 
#	float Open;
#	float High;
#	float Low;
#	float Close;
#	uint32_t NumTrades;
#	uint32_t TotalVolume;
#	uint32_t BidVolume;
#	uint32_t AskVolume;
#}
ir_format = 'QffffLLLL'
ir_len = struct.calcsize(ir_format)

def read_hdr(file):
    file.seek(0, 2) # move to end of file
    file_length_remaining = file.tell() # get current position
    file.seek(0, 0) # go back to where we started

    header = file.read(ifh_len)
    hdr_tuple = unpack(ifh_format, header)
    return hdr_tuple

def read_ir(file):
    ir = file.read(ir_len)
    if len(ir) < ir_len:
        return None
    ir_tuple = unpack(ir_format, ir)
    return ir_tuple




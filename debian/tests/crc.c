#include <stdio.h>
#include <isa-l/crc.h>

int main(void)
{
	const unsigned char data[] = "abcde";
	const uint32_t want = 383173788;

	uint32_t count = crc32_ieee(0, data, sizeof(data));

	if (count != want) {
		printf("%d != %d", count, want);
		return 1;
	} else {
		return 0;
	}
}

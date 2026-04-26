# Secure Password Criteria and Examples

## General Password Rules
A secure password must meet these baseline criteria:
- Minimum 8 characters (12+ strongly recommended)
- Mix of uppercase and lowercase letters
- At least one digit (0-9)
- At least one special character (!@#$%^&*) for non-PIN use cases
- No dictionary words or common patterns (123456, qwerty, password)
- No personal information (name, birthdate, username)
- Avoid repeating characters or sequential runs

## Character Classes

### Uppercase Letters
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Use at least 2 uppercase letters spread throughout the password, not just at the start.

### Lowercase Letters
a b c d e f g h i j k l m n o p q r s t u v w x y z
Lowercase forms the bulk of most passwords. Vary placement.

### Digits
0 1 2 3 4 5 6 7 8 9
Embed digits mid-password rather than appending them at the end (e.g. avoid "Password1").

### Safe Special Characters
! @ # $ % ^ & * - _ + = ?
These are widely accepted across most systems. Avoid spaces, < > / \ | ` ~ which cause parsing issues.

### Ambiguous Characters to Avoid for Readability
0 vs O, 1 vs l vs I — skip these in human-readable passwords to prevent confusion.

## Length Guidelines by Use Case

### PIN / Numeric
- Length: 4-8 digits
- Only digits (0-9)
- Avoid patterns: 1234, 0000, repeated digits, birth years
- Example strong PINs: 8372, 49201, 730846

### WiFi / Network Password
- Minimum 12 characters
- Mix of letters and numbers; symbols optional but recommended
- Should be memorable enough to share but hard to guess
- Example: Nx7kP2mQr4wJ, blue-monkey-42

### Social Media
- Minimum 12 characters
- Uppercase + lowercase + digits + symbols
- Unique per platform — never reuse social passwords
- Example: Tr@nquil9Moon, W1nter!Hawk22

### Banking / Financial
- Minimum 14 characters, alphanumeric only (many banks reject symbols)
- High entropy, no patterns, no personal info
- Example: Kv3mPxN8qR2sLt, BrightFalcon24X

### Work / Enterprise
- Minimum 16 characters
- Full complexity: uppercase + lowercase + digits + symbols
- Rotate every 90 days; never reuse last 10 passwords
- Example: Z@phr7Luna#Tide93, Ember$Vortex!25Kq

### High Security / Passphrase
- 20+ characters
- Multiple unrelated words combined with numbers and symbols
- Passphrases balance memorability with high entropy
- Example: correct-horse-Battery!9, Purple!Mango-Orbit77

## Entropy and Strength Levels

### Weak (under 40 bits)
- Short, single character class, common words
- Example: abc123, password1, 12345678

### Fair (40-60 bits)
- 8-10 chars, 2 character classes
- Example: BlueSky99, market$22

### Strong (60-80 bits)
- 12-16 chars, 3 or more character classes
- Example: T3mpl@rBlaze!, NightOwl#2024

### Very Strong (80+ bits)
- 16+ chars, full complexity, no patterns
- Example: Cr1mson$Vortex!Hawk83, Z@phr7!Luna#Tide93Wq

## Anti-Patterns to Avoid
- Keyboard walks: qwerty, asdfgh, zxcvbn, 1qaz2wsx
- Sequential numbers: 123456, 654321, 111222
- Repeated characters: aaaa, 1111, !!!! 
- Common substitutions that are already known to attackers: p@ssw0rd, S3cur3, @dmin
- Name + year format: John2024, Maria1990, Alex2000
- Company name variations: Google123!, Faceb00k, Micros0ft
- Single dictionary word with a number appended: monkey1, dragon99

## NIST 2024 Guidelines
- Prefer length over complexity for memorability
- 15+ characters is the current minimum recommendation
- Passphrases (multiple unrelated words) are encouraged for human-remembered passwords
- Mandatory complexity rules alone (must have a symbol) are less important than length
- Check passwords against known breach databases (HaveIBeenPwned)
- Do not require periodic rotation unless there is evidence of compromise
- Allow all printable ASCII characters and spaces in passwords

import { tokens } from "@team2/shared";
import { Button } from "@team2/ui";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Home() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.title}>19th-team2</Text>
        <Text style={styles.description}>Expo + 공용 UI(@team2/ui)</Text>
        <Button label="공용 Button" onPress={() => {}} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: tokens.color.background },
  container: { flex: 1, alignItems: "center", justifyContent: "center", gap: 16, padding: 16 },
  title: { fontSize: 24, fontWeight: "700", color: tokens.color.foreground },
  description: { color: tokens.color["muted-foreground"] },
});
